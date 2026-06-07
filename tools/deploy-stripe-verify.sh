#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/workers/stripe-verify"

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  echo "Missing CLOUDFLARE_API_TOKEN."
  echo "Create at: https://dash.cloudflare.com/profile/api-tokens"
  echo "Permissions: Account / Cloudflare Workers Scripts / Edit"
  exit 1
fi

if [[ -z "${STRIPE_SECRET_KEY:-}" ]]; then
  echo "Missing STRIPE_SECRET_KEY (sk_live_... or rk_live_...)."
  exit 1
fi

npx wrangler deploy
printf '%s' "$STRIPE_SECRET_KEY" | npx wrangler secret put STRIPE_SECRET_KEY

echo ""
echo "Worker deployed. Default URL:"
npx wrangler deployments list 2>/dev/null | head -5 || true
echo ""
echo "Set verifyEndpoint in index.html PAYMENT_CONFIG to:"
echo "  https://muxtext-stripe-verify.<your-subdomain>.workers.dev"
echo "Then set allowLiveTrustRedirect: false"
