#!/usr/bin/env node
/**
 * Create Stripe Payment Links for overload chip packages.
 * Usage: STRIPE_SECRET_KEY=sk_test_... node tools/setup-stripe-payment-links.mjs
 * Never commit the secret key — only paste the printed stripeLink URLs into index.html.
 */
const SECRET = process.env.STRIPE_SECRET_KEY;
const SUCCESS_BASE = process.env.STRIPE_SUCCESS_BASE || 'https://muexostudios-cell.github.io/Muxtext/';

const CHIP_RATE = 1280 / 148; // chips per HKD from top existing tier

const PACKAGES = [
  { id: 'chip60', chips: 60, priceHkd: 8 },
  { id: 'chip300', chips: 300, priceHkd: 38 },
  { id: 'chip680', chips: 680, priceHkd: 78 },
  { id: 'chip1280', chips: 1280, priceHkd: 148 },
  { id: 'chip1712', chips: Math.round(198 * CHIP_RATE), priceHkd: 198 },
  { id: 'chip2837', chips: Math.round(328 * CHIP_RATE), priceHkd: 328 },
  { id: 'chip3875', chips: Math.round(448 * CHIP_RATE), priceHkd: 448 },
  { id: 'chip5604', chips: Math.round(648 * CHIP_RATE), priceHkd: 648 },
];

if (!SECRET) {
  console.error('Set STRIPE_SECRET_KEY (sk_test_... or sk_live_...)');
  process.exit(1);
}

async function stripePost(path, params) {
  const body = new URLSearchParams(params);
  const res = await fetch(`https://api.stripe.com/v1${path}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${SECRET}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error?.message || res.statusText);
  return data;
}

async function main() {
  const product = await stripePost('/products', {
    name: 'MUX 超載晶片',
    description: 'MUX text-rpg Overload Chips',
  });
  console.log('Product:', product.id);

  const links = [];
  for (const pkg of PACKAGES) {
    const price = await stripePost('/prices', {
      product: product.id,
      unit_amount: String(pkg.priceHkd * 100),
      currency: 'hkd',
      nickname: `${pkg.chips} chips`,
    });
    const successUrl = `${SUCCESS_BASE}?overload_success=${pkg.id}&session_id={CHECKOUT_SESSION_ID}`;
    const link = await stripePost('/payment_links', {
      'line_items[0][price]': price.id,
      'line_items[0][quantity]': '1',
      'after_completion[type]': 'redirect',
      'after_completion[redirect][url]': successUrl,
      'metadata[package_id]': pkg.id,
      'metadata[chips]': String(pkg.chips),
    });
    links.push({ ...pkg, stripeLink: link.url, priceId: price.id });
    console.log(`${pkg.id}: ${link.url}`);
  }

  console.log('\nPaste into OVERLOAD_CHIP_PACKAGES in index.html:');
  console.log(
    links
      .map(
        (p) =>
          `{id:'${p.id}',chips:${p.chips},priceLabel:'HK$${p.priceHkd}',priceHkd:${p.priceHkd},stripeLink:'${p.stripeLink}',stripePriceId:'${p.priceId}'}`
      )
      .join(',')
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
