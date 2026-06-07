/**
 * Stripe checkout session verification for MUX text-rpg.
 * Deploy with Wrangler; set STRIPE_SECRET_KEY (sk_live_...) as a secret.
 *
 *   cd workers/stripe-verify
 *   npx wrangler secret put STRIPE_SECRET_KEY
 *   npx wrangler deploy
 */
const PACKAGE_CATALOG = {
  chip60: { chips: 60, hkd: 8 },
  chip300: { chips: 300, hkd: 38 },
  chip680: { chips: 680, hkd: 78 },
  chip1280: { chips: 1280, hkd: 148 },
  chip1712: { chips: 1712, hkd: 198 },
  chip2837: { chips: 2837, hkd: 328 },
  chip3875: { chips: 3875, hkd: 448 },
  chip5604: { chips: 5604, hkd: 648 },
};

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }
    if (request.method !== 'POST') {
      return json({ error: 'method_not_allowed' }, 405);
    }
    if (!env.STRIPE_SECRET_KEY) {
      return json({ error: 'server_not_configured' }, 503);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ error: 'invalid_json' }, 400);
    }

    const sessionId = body.sessionId;
    const packageId = body.packageId;
    if (!sessionId || !packageId) {
      return json({ error: 'missing_fields' }, 400);
    }
    if (!sessionId.startsWith('cs_')) {
      return json({ error: 'invalid_session' }, 400);
    }

    const catalog = PACKAGE_CATALOG[packageId];
    if (!catalog) {
      return json({ error: 'unknown_package' }, 400);
    }

    const stripeRes = await fetch(
      `https://api.stripe.com/v1/checkout/sessions/${encodeURIComponent(sessionId)}`,
      { headers: { Authorization: `Bearer ${env.STRIPE_SECRET_KEY}` } }
    );
    const session = await stripeRes.json();
    if (!stripeRes.ok) {
      return json({ error: session.error?.message || 'stripe_error' }, 502);
    }

    if (session.payment_status !== 'paid') {
      return json({ error: 'not_paid', status: session.payment_status }, 402);
    }

    const refPkg = session.metadata?.package_id || session.client_reference_id || '';
    if (refPkg && refPkg !== packageId) {
      return json({ error: 'package_mismatch' }, 400);
    }

    const expectedCents = catalog.hkd * 100;
    if (session.amount_total != null && session.amount_total !== expectedCents) {
      return json({ error: 'amount_mismatch' }, 400);
    }

    const metaChips = parseInt(session.metadata?.chips || '0', 10);
    const chips = metaChips > 0 ? metaChips : catalog.chips;
    if (chips !== catalog.chips) {
      return json({ error: 'chips_mismatch' }, 400);
    }

    return json({
      paid: true,
      chips,
      orderId: sessionId,
      packageId,
      livemode: !!session.livemode,
    });
  },
};
