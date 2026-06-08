/**
 * MUX text-rpg · independent chat backend (Cloudflare Worker + Durable Object).
 *
 * Deploy:
 *   cd workers/chat
 *   npx wrangler deploy
 *
 * Set CHAT_CONFIG.endpoint in index.html to:
 *   https://muxtext-chat.<your-subdomain>.workers.dev
 */
const MAX_MESSAGES = 100;
const MAX_TEXT = 200;
const MAX_USER = 32;
const MAX_LEVEL = 99999;
const MAX_PROFILE_BYTES = 20000;
const SEND_COOLDOWN_MS = 1500;

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function withCors(response) {
  const headers = new Headers(response.headers);
  Object.entries(CORS_HEADERS).forEach(([k, v]) => headers.set(k, v));
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}

function json(data, status = 200, extraHeaders = {}) {
  return withCors(
    new Response(JSON.stringify(data), {
      status,
      headers: { 'Content-Type': 'application/json', ...extraHeaders },
    })
  );
}

function sanitizeLevel(value) {
  const n = parseInt(value, 10);
  if (!Number.isFinite(n) || n < 1) return null;
  return Math.min(n, MAX_LEVEL);
}

const PROFILE_RARITIES = new Set(['common', 'rare', 'epic', 'legendary', 'hidden']);

function clampInt(value, min, max, fallback = 0) {
  const n = parseInt(value, 10);
  if (!Number.isFinite(n)) return fallback;
  return Math.min(max, Math.max(min, n));
}

function sanitizeAvatarUrl(url) {
  if (!url || typeof url !== 'string') return '';
  const trimmed = url.trim();
  if (!trimmed.startsWith('data:image/') || trimmed.length > 8000) return '';
  return trimmed;
}

function sanitizeEquipItem(raw) {
  if (!raw || typeof raw !== 'object') return null;
  const affixes = Array.isArray(raw.affixes)
    ? raw.affixes.slice(0, 8).map((a) => ({
        stat: String(a?.stat || '').slice(0, 24),
        value: Number(a?.value) || 0,
      }))
    : [];
  return {
    name: String(raw.name || '').slice(0, 40),
    rarity: PROFILE_RARITIES.has(raw.rarity) ? raw.rarity : 'common',
    type: String(raw.type || '').slice(0, 16),
    level: clampInt(raw.level, 1, MAX_LEVEL, 1),
    upgradeLv: clampInt(raw.upgradeLv, 0, 99, 0),
    baseStat: String(raw.baseStat || '').slice(0, 24),
    baseValue: Number(raw.baseValue) || 0,
    affixes,
  };
}

function sanitizeProfile(raw) {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return null;

  const profile = {
    n: String(raw.n || raw.name || '???').slice(0, MAX_USER),
    lv: clampInt(raw.lv ?? raw.level, 1, MAX_LEVEL, 1),
    g: Math.max(0, clampInt(raw.g ?? raw.gold, 0, 999999999, 0)),
    c: Math.max(0, clampInt(raw.c ?? raw.chips, 0, 999999999, 0)),
    cl: clampInt(raw.cl ?? raw.craftLevel, 1, MAX_LEVEL, 1),
    dl: clampInt(raw.dl ?? raw.droneIdleLevel, 1, MAX_LEVEL, 1),
    md: Math.min(100, Math.max(0, Number(raw.md ?? raw.memoryDecay) || 0)),
    atk: Math.max(0, clampInt(raw.atk, 0, 999999, 0)),
    def: Math.max(0, clampInt(raw.def, 0, 999999, 0)),
    hp: Math.max(0, clampInt(raw.hp, 0, 999999, 0)),
    spd: Math.max(0, clampInt(raw.spd, 0, 999999, 0)),
    crit: Math.max(0, clampInt(raw.crit, 0, 100, 0)),
    dodge: Math.max(0, clampInt(raw.dodge, 0, 100, 0)),
    talents: {},
    equip: {},
    st: {},
  };

  const avatar = sanitizeAvatarUrl(raw.av || raw.avatar);
  if (avatar) profile.av = avatar;

  if (raw.talents && typeof raw.talents === 'object') {
    for (const key of Object.keys(raw.talents).slice(0, 12)) {
      profile.talents[key] = Math.max(0, clampInt(raw.talents[key], 0, 9999, 0));
    }
  }

  if (raw.equip && typeof raw.equip === 'object') {
    for (const slot of Object.keys(raw.equip).slice(0, 12)) {
      const item = sanitizeEquipItem(raw.equip[slot]);
      if (item) profile.equip[slot] = item;
    }
  }

  const stats = raw.st || raw.stats || {};
  profile.st = {
    ca: clampInt(stats.ca ?? stats.createdAt, 0, 9999999999999, 0),
    pt: Math.max(0, clampInt(stats.pt ?? stats.totalPlaytime, 0, 999999999, 0)),
    dc: Math.max(0, clampInt(stats.dc ?? stats.dungeonClears, 0, 999999999, 0)),
    dk: Math.max(0, clampInt(stats.dk ?? stats.dungeonKills, 0, 999999999, 0)),
  };

  let serialized;
  try {
    serialized = JSON.stringify(profile);
  } catch {
    return null;
  }
  if (!serialized || serialized.length > MAX_PROFILE_BYTES) return null;
  return profile;
}

export class ChatRoom {
  constructor(ctx) {
    this.ctx = ctx;
    this.sessions = new Set();
  }

  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return withCors(new Response(null, { status: 204 }));
    }

    if (url.pathname === '/health' && request.method === 'GET') {
      return json({ ok: true }, 200, { 'Cache-Control': 'public, max-age=30' });
    }

    if (url.pathname === '/messages' && request.method === 'GET') {
      const messages = await this.getMessages();
      const after = parseInt(url.searchParams.get('after') || '0', 10);
      const limit = Math.min(parseInt(url.searchParams.get('limit') || '50', 10), MAX_MESSAGES);
      let list = after > 0 ? messages.filter((m) => m.time > after) : messages.slice(-limit);
      const cacheControl = after > 0 ? 'private, max-age=0' : 'public, max-age=3';
      return json({ messages: list }, 200, { 'Cache-Control': cacheControl });
    }

    if (url.pathname === '/messages' && request.method === 'POST') {
      const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
      const allowed = await this.checkRateLimit(ip);
      if (!allowed) {
        return json({ error: 'rate_limited' }, 429);
      }

      let body;
      try {
        body = await request.json();
      } catch {
        return json({ error: 'invalid_json' }, 400);
      }

      const user = String(body.user || 'PLAYER').trim().slice(0, MAX_USER) || 'PLAYER';
      const text = String(body.text || '').trim().slice(0, MAX_TEXT);
      if (!text) {
        return json({ error: 'empty' }, 400);
      }

      const level = sanitizeLevel(body.level);
      const profile = sanitizeProfile(body.profile);

      const msg = {
        id: crypto.randomUUID(),
        user,
        text,
        time: Date.now(),
      };
      if (level != null) msg.level = level;
      if (profile) msg.profile = profile;

      await this.addMessage(msg);
      this.broadcast({ type: 'message', data: msg });
      return json({ ok: true, message: msg });
    }

    if (url.pathname === '/ws' && request.headers.get('Upgrade') === 'websocket') {
      const pair = new WebSocketPair();
      const client = pair[0];
      const server = pair[1];
      this.handleSession(server);
      return new Response(null, { status: 101, webSocket: client });
    }

    return json({ error: 'not_found' }, 404);
  }

  async getMessages() {
    const stored = await this.ctx.storage.get('messages');
    return Array.isArray(stored) ? stored : [];
  }

  async addMessage(msg) {
    const messages = await this.getMessages();
    messages.push(msg);
    while (messages.length > MAX_MESSAGES) {
      messages.shift();
    }
    await this.ctx.storage.put('messages', messages);
  }

  async checkRateLimit(ip) {
    const key = `rate:${ip}`;
    const last = (await this.ctx.storage.get(key)) || 0;
    const now = Date.now();
    if (now - last < SEND_COOLDOWN_MS) {
      return false;
    }
    await this.ctx.storage.put(key, now);
    return true;
  }

  handleSession(ws) {
    ws.accept();
    this.sessions.add(ws);
    ws.addEventListener('close', () => this.sessions.delete(ws));
    ws.addEventListener('error', () => this.sessions.delete(ws));
  }

  broadcast(payload) {
    const data = JSON.stringify(payload);
    for (const ws of this.sessions) {
      try {
        ws.send(data);
      } catch {
        this.sessions.delete(ws);
      }
    }
  }
}

export default {
  async fetch(request, env) {
    const id = env.CHAT_ROOM.idFromName('nightcity-global');
    const stub = env.CHAT_ROOM.get(id);
    return stub.fetch(request);
  },
};
