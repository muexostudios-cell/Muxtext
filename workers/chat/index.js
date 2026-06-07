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
const MAX_PROFILE_BYTES = 12000;
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

function json(data, status = 200) {
  return withCors(
    new Response(JSON.stringify(data), {
      status,
      headers: { 'Content-Type': 'application/json' },
    })
  );
}

function sanitizeLevel(value) {
  const n = parseInt(value, 10);
  if (!Number.isFinite(n) || n < 1) return null;
  return Math.min(n, MAX_LEVEL);
}

function sanitizeProfile(raw) {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return null;
  let serialized;
  try {
    serialized = JSON.stringify(raw);
  } catch {
    return null;
  }
  if (!serialized || serialized.length > MAX_PROFILE_BYTES) return null;
  try {
    return JSON.parse(serialized);
  } catch {
    return null;
  }
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
      return json({ ok: true });
    }

    if (url.pathname === '/messages' && request.method === 'GET') {
      const messages = await this.getMessages();
      const after = parseInt(url.searchParams.get('after') || '0', 10);
      const limit = Math.min(parseInt(url.searchParams.get('limit') || '50', 10), MAX_MESSAGES);
      let list = after > 0 ? messages.filter((m) => m.time > after) : messages.slice(-limit);
      return json({ messages: list });
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
