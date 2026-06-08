/**
 * MUX text-rpg · Bug lifecycle pipeline (Cloudflare Worker + Durable Object).
 *
 * Ingests client reports, probes dependencies, rule/AI triage, lifecycle tracking.
 *
 * Deploy:
 *   cd workers/bug-pipeline
 *   npx wrangler deploy
 *   npx wrangler secret put OPENAI_API_KEY   # optional — enables AI triage
 *
 * Set BUG_PIPELINE_CONFIG.endpoint in index.html to workers.dev URL.
 */
import { KNOWN_BUGS, LIFECYCLE_STAGES, matchBugBySignals, matchBugByText } from './known-bugs.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

const MAX_REPORTS = 500;
const MAX_TEXT = 2000;
const CLUSTER_THRESHOLD = 3;
const CONFIRM_THRESHOLD = 5;

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

function withCors(response) {
  const headers = new Headers(response.headers);
  Object.entries(CORS_HEADERS).forEach(([k, v]) => headers.set(k, v));
  return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
}

function sanitizeText(value, max = MAX_TEXT) {
  return String(value || '').slice(0, max);
}

function nowIso() {
  return new Date().toISOString();
}

async function probeUrl(url, timeoutMs = 8000) {
  if (!url) return { ok: false, status: 0, error: 'no_url' };
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const res = await fetch(url, { signal: ctrl.signal, headers: { 'User-Agent': 'muxtext-bug-pipeline/1.0' } });
    clearTimeout(timer);
    return { ok: res.ok, status: res.status, error: res.ok ? null : `http_${res.status}` };
  } catch (e) {
    clearTimeout(timer);
    return { ok: false, status: 0, error: e.name === 'AbortError' ? 'timeout' : 'fetch_error' };
  }
}

async function runServerProbes(env) {
  const chatUrl = env.CHAT_HEALTH_URL || '';
  const gameUrl = env.GAME_HEALTH_URL || 'https://muexostudios-cell.github.io/Muxtext/';
  const stripeUrl = env.STRIPE_VERIFY_HEALTH_URL || '';

  const [chat, game, stripe] = await Promise.all([
    probeUrl(chatUrl ? `${chatUrl.replace(/\/$/, '')}/health` : ''),
    probeUrl(gameUrl),
    probeUrl(stripeUrl ? `${stripeUrl.replace(/\/$/, '')}/health` : stripeUrl),
  ]);

  const signals = [];
  if (chatUrl && !chat.ok) signals.push('chat_worker_down');
  if (!game.ok) signals.push('game_host_down');
  if (stripeUrl && !stripe.ok) signals.push('stripe_verify_down');
  if (!stripeUrl) signals.push('stripe_verify_unconfigured');

  return {
    at: nowIso(),
    chat: chatUrl ? chat : { ok: null, skipped: true },
    game,
    stripe: stripeUrl ? stripe : { ok: null, skipped: true },
    signals,
  };
}

function ruleTriage(report, probe, lifecycle) {
  const signals = [...(report.signals || []), ...(probe?.signals || [])];
  const bug =
    matchBugBySignals(signals) ||
    matchBugByText(report.message) ||
    matchBugByText(report.stack) ||
    null;

  const bugId = bug?.id || 'unknown';
  const entry = lifecycle[bugId] || {
    bugId,
    stage: 'reported',
    reportCount: 0,
    firstSeen: nowIso(),
    lastSeen: nowIso(),
    serverConfirmed: false,
    fixVersion: bug?.fixedVersion || null,
  };

  entry.reportCount += 1;
  entry.lastSeen = nowIso();
  entry.lastSignals = signals.slice(0, 20);
  entry.summary = bug?.summary || { zh: '未分類問題', en: 'Unclassified issue' };
  entry.severity = bug?.severity || 'low';
  entry.category = bug?.category || 'unknown';

  const serverHit = bug?.serverSignals?.some((s) => signals.includes(s));
  const clientOnly = bug && bug.serverSignals.length === 0 && !serverHit;

  if (entry.reportCount >= CONFIRM_THRESHOLD && serverHit) {
    entry.stage = 'confirmed';
    entry.serverConfirmed = true;
  } else if (entry.reportCount >= CLUSTER_THRESHOLD) {
    entry.stage = serverHit ? 'probing' : clientOnly ? 'client-only' : 'clustered';
  }

  if (probe && serverHit && !probe.chat?.skipped && probe.chat && !probe.chat.ok && bugId === 'chat-offline') {
    entry.stage = 'confirmed';
    entry.serverConfirmed = true;
  }
  if (probe && !probe.game?.ok && bugId === 'game-host-down') {
    entry.stage = 'confirmed';
    entry.serverConfirmed = true;
  }

  if (bug?.fixedVersion && entry.stage !== 'confirmed') {
    entry.stage = 'fixed';
    entry.fixVersion = bug.fixedVersion;
  }

  lifecycle[bugId] = entry;
  return { bugId, entry, confidence: entry.reportCount >= CONFIRM_THRESHOLD ? 'high' : entry.reportCount >= CLUSTER_THRESHOLD ? 'medium' : 'low' };
}

async function aiTriage(env, report, ruleResult) {
  if (!env.OPENAI_API_KEY) return null;
  const prompt = `You triage MUX text-rpg bug reports. Reply JSON only: {"isServerIssue":bool,"severity":"low|medium|high|critical","bugId":"${ruleResult.bugId}","summary":"one line","action":"monitor|investigate|hotfix"}\nReport: ${JSON.stringify({ message: report.message, signals: report.signals, gameVersion: report.gameVersion })}`;
  try {
    const res = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.OPENAI_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4o-mini',
        temperature: 0,
        messages: [
          { role: 'system', content: 'Bug triage for a browser text RPG. JSON only.' },
          { role: 'user', content: prompt },
        ],
      }),
    });
    if (!res.ok) return null;
    const data = await res.json();
    const text = data.choices?.[0]?.message?.content || '';
    const match = text.match(/\{[\s\S]*\}/);
    if (!match) return null;
    return JSON.parse(match[0]);
  } catch {
    return null;
  }
}

export class BugLifecycleStore {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async fetch(request) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/$/, '') || '/';

    if (request.method === 'GET' && path === '/status') {
      const data = (await this.state.storage.get('data')) || defaultStore();
      return json({
        ok: true,
        lifecycle: data.lifecycle,
        lastProbe: data.lastProbe,
        activeIssues: buildActiveIssues(data),
        stages: LIFECYCLE_STAGES,
        knownBugs: KNOWN_BUGS.map((b) => ({
          id: b.id,
          severity: b.severity,
          fixedVersion: b.fixedVersion,
          summary: b.summary,
        })),
      });
    }

    if (request.method === 'POST' && path === '/report') {
      let body;
      try {
        body = await request.json();
      } catch {
        return json({ error: 'invalid_json' }, 400);
      }
      const data = (await this.state.storage.get('data')) || defaultStore();
      const report = {
        id: crypto.randomUUID(),
        at: nowIso(),
        gameVersion: sanitizeText(body.gameVersion, 16),
        saveVersion: Number(body.saveVersion) || 0,
        message: sanitizeText(body.message, 500),
        stack: sanitizeText(body.stack, 1000),
        signals: Array.isArray(body.signals) ? body.signals.slice(0, 30).map((s) => sanitizeText(s, 64)) : [],
        context: typeof body.context === 'object' && body.context ? body.context : {},
        source: sanitizeText(body.source, 32) || 'client',
      };
      data.reports.unshift(report);
      if (data.reports.length > MAX_REPORTS) data.reports.length = MAX_REPORTS;

      const ruleResult = ruleTriage(report, data.lastProbe, data.lifecycle);
      let ai = null;
      if (data.reports.length % 5 === 0 || ruleResult.entry.reportCount >= CLUSTER_THRESHOLD) {
        ai = await aiTriage(this.env, report, ruleResult);
        if (ai?.isServerIssue && ruleResult.entry.stage === 'clustered') {
          ruleResult.entry.stage = 'confirmed';
          ruleResult.entry.serverConfirmed = true;
          ruleResult.entry.aiSummary = sanitizeText(ai.summary, 200);
        }
      }
      data.lifecycle[ruleResult.bugId] = ruleResult.entry;
      await this.state.storage.put('data', data);

      return json({
        ok: true,
        reportId: report.id,
        bugId: ruleResult.bugId,
        stage: ruleResult.entry.stage,
        serverConfirmed: ruleResult.entry.serverConfirmed,
        fixVersion: ruleResult.entry.fixVersion,
        confidence: ruleResult.confidence,
        ai,
      });
    }

    if (request.method === 'POST' && path === '/probe') {
      const auth = request.headers.get('Authorization') || '';
      const cron = request.headers.get('cf-worker-cron') || request.headers.get('CF-Worker-Cron');
      if (!cron && auth !== `Bearer ${this.env.PROBE_SECRET || ''}` && this.env.PROBE_SECRET) {
        return json({ error: 'unauthorized' }, 401);
      }
      const data = (await this.state.storage.get('data')) || defaultStore();
      data.lastProbe = await runServerProbes(this.env);
      for (const report of data.reports.slice(0, 50)) {
        ruleTriage(report, data.lastProbe, data.lifecycle);
      }
      data.lastProbeAt = nowIso();
      await this.state.storage.put('data', data);
      return json({ ok: true, probe: data.lastProbe, activeIssues: buildActiveIssues(data) });
    }

    return json({ error: 'not_found' }, 404);
  }
}

function defaultStore() {
  return { reports: [], lifecycle: {}, lastProbe: null, lastProbeAt: null };
}

function buildActiveIssues(data) {
  return Object.values(data.lifecycle || {})
    .filter((e) => ['clustered', 'probing', 'confirmed'].includes(e.stage))
    .sort((a, b) => {
      const sev = { critical: 0, high: 1, medium: 2, low: 3 };
      return (sev[a.severity] || 9) - (sev[b.severity] || 9);
    })
    .slice(0, 12);
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname.replace(/\/$/, '') || '/';

    if (path === '/health') {
      return json({ ok: true, service: 'muxtext-bug-pipeline', at: nowIso() });
    }

    const id = env.BUG_STORE.idFromName('global');
    const stub = env.BUG_STORE.get(id);
    const doPath = path === '/status' ? '/status' : path === '/report' ? '/report' : path === '/probe' ? '/probe' : null;

    if (doPath) {
      const doUrl = new URL(request.url);
      doUrl.pathname = doPath;
      return withCors(await stub.fetch(new Request(doUrl.toString(), request)));
    }

    return json({ error: 'not_found' }, 404);
  },

  async scheduled(event, env, ctx) {
    const id = env.BUG_STORE.idFromName('global');
    const stub = env.BUG_STORE.get(id);
    const req = new Request('https://bug-pipeline/probe', {
      method: 'POST',
      headers: { 'CF-Worker-Cron': '1' },
    });
    ctx.waitUntil(stub.fetch(req));
  },
};
