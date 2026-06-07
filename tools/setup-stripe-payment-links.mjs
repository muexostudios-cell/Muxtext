#!/usr/bin/env node
/**
 * Create Stripe Payment Links for overload chip packages.
 *
 * Test:  STRIPE_SECRET_KEY=sk_test_... node tools/setup-stripe-payment-links.mjs
 * Live:  STRIPE_SECRET_KEY=sk_live_... node tools/setup-stripe-payment-links.mjs --mode live
 *
 * Optional:
 *   STRIPE_PRODUCT_ID=prod_xxx   reuse existing product
 *   STRIPE_SUCCESS_BASE=https://muexostudios-cell.github.io/Muxtext/
 *   --write-index                patch index.html (stripeLinkTest or stripeLinkLive)
 *
 * Never commit secret keys.
 */
import { readFileSync, writeFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const INDEX_PATH = join(ROOT, 'index.html');

const SECRET = process.env.STRIPE_SECRET_KEY;
const SUCCESS_BASE = process.env.STRIPE_SUCCESS_BASE || 'https://muexostudios-cell.github.io/Muxtext/';
const PRODUCT_ID = process.env.STRIPE_PRODUCT_ID || '';
const modeArg = process.argv.includes('--mode') ? process.argv[process.argv.indexOf('--mode') + 1] : '';
const WRITE_INDEX = process.argv.includes('--write-index');
const MODE = modeArg === 'live' || (SECRET && SECRET.startsWith('sk_live_')) ? 'live' : 'test';
const LINK_FIELD = MODE === 'live' ? 'stripeLinkLive' : 'stripeLinkTest';

const CHIP_RATE = 1280 / 148;

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

function patchIndexHtml(links) {
  let html = readFileSync(INDEX_PATH, 'utf8');
  for (const p of links) {
    const re = new RegExp(
      `(\\{id:'${p.id}'[^}]*${LINK_FIELD}:)'[^']*'`,
      'g'
    );
    if (!re.test(html)) {
      // migrate legacy stripeLink -> stripeLinkTest on first live run
      const legacy = new RegExp(`(\\{id:'${p.id}'[^}]*stripeLink:)'[^']*'`);
      if (legacy.test(html) && LINK_FIELD === 'stripeLinkTest') {
        html = html.replace(legacy, `$1'${p.stripeLink}'`);
        continue;
      }
      console.warn(`Could not patch ${p.id} — update index.html manually`);
      continue;
    }
    html = readFileSync(INDEX_PATH, 'utf8');
    html = html.replace(
      new RegExp(`(\\{id:'${p.id}'[^}]*${LINK_FIELD}:)'[^']*'`),
      `$1'${p.stripeLink}'`
    );
    writeFileSync(INDEX_PATH, html);
  }
  if (MODE === 'live') {
    let latest = readFileSync(INDEX_PATH, 'utf8');
    if (latest.includes("mode:'test'") || latest.includes('mode:"test"')) {
      latest = latest.replace(/mode:'test'/, "mode:'live'");
      writeFileSync(INDEX_PATH, latest);
      console.log("Set PAYMENT_CONFIG.mode to 'live'");
    }
  }
}

async function main() {
  console.log(`Mode: ${MODE} (${LINK_FIELD})`);

  const product = PRODUCT_ID
    ? { id: PRODUCT_ID }
    : await stripePost('/products', {
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

  if (WRITE_INDEX) {
    patchIndexHtml(links);
    console.log(`\nUpdated ${INDEX_PATH}`);
  } else {
    console.log('\nAdd to index.html (' + LINK_FIELD + ' per package):');
    links.forEach((p) => console.log(`  ${p.id}: ${p.stripeLink}`));
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
