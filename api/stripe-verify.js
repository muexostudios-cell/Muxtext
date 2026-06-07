/**
 * Vercel serverless fallback for Stripe checkout verification.
 * Deploy: vercel --prod  →  set STRIPE_SECRET_KEY in Vercel env
 * Endpoint: https://<project>.vercel.app/api/stripe-verify
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

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(res, data, status = 200) {
  res.statusCode = status;
  Object.entries({ 'Content-Type': 'application/json', ...CORS }).forEach(([k, v]) =>
    res.setHeader(k, v)
  );
  res.end(JSON.stringify(data));
}

module.exports = async (req, res) => {
  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    Object.entries(CORS).forEach(([k, v]) => res.setHeader(k, v));
    return res.end();
  }
  if (req.method !== 'POST') return json(res, { error: 'method_not_allowed' }, 405);

  const secret = process.env.STRIPE_SECRET_KEY;
  if (!secret) return json(res, { error: 'server_not_configured' }, 503);

  let body;
  try {
    body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body || {};
  } catch {
    return json(res, { error: 'invalid_json' }, 400);
  }

  const { sessionId, packageId } = body;
  if (!sessionId || !packageId) return json(res, { error: 'missing_fields' }, 400);
  if (!sessionId.startsWith('cs_')) return json(res, { error: 'invalid_session' }, 400);

  const catalog = PACKAGE_CATALOG[packageId];
  if (!catalog) return json(res, { error: 'unknown_package' }, 400);

  const stripeRes = await fetch(
    `https://api.stripe.com/v1/checkout/sessions/${encodeURIComponent(sessionId)}`,
    { headers: { Authorization: `Bearer ${secret}` } }
  );
  const session = await stripeRes.json();
  if (!stripeRes.ok) return json(res, { error: session.error?.message || 'stripe_error' }, 502);
  if (session.payment_status !== 'paid') {
    return json(res, { error: 'not_paid', status: session.payment_status }, 402);
  }

  const refPkg = session.metadata?.package_id || session.client_reference_id || '';
  if (refPkg && refPkg !== packageId) return json(res, { error: 'package_mismatch' }, 400);

  const expectedCents = catalog.hkd * 100;
  if (session.amount_total != null && session.amount_total !== expectedCents) {
    return json(res, { error: 'amount_mismatch' }, 400);
  }

  const metaChips = parseInt(session.metadata?.chips || '0', 10);
  const chips = metaChips > 0 ? metaChips : catalog.chips;
  if (chips !== catalog.chips) return json(res, { error: 'chips_mismatch' }, 400);

  return json(res, {
    paid: true,
    chips,
    orderId: sessionId,
    packageId,
    livemode: !!session.livemode,
  });
};
