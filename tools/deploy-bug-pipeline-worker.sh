#!/usr/bin/env bash
# Deploy muxtext-bug-pipeline Worker and write workers.dev URL into index.html.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKER_DIR="$ROOT/workers/bug-pipeline"
INDEX="$ROOT/index.html"

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  echo "Missing CLOUDFLARE_API_TOKEN."
  echo ""
  echo "One-command setup (auto-resolves Account ID):"
  echo "  CLOUDFLARE_API_TOKEN=... bash tools/setup-cloudflare-auto.sh"
  echo ""
  echo "Create token: https://dash.cloudflare.com/profile/api-tokens"
  echo "  Template: Edit Cloudflare Workers"
  exit 1
fi

if [[ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]]; then
  CLOUDFLARE_ACCOUNT_ID="$(bash "$(dirname "$0")/cloudflare-resolve-account.sh")"
  if [[ -z "$CLOUDFLARE_ACCOUNT_ID" ]]; then
    echo "Could not resolve Account ID from API token." >&2
    exit 1
  fi
  echo "Resolved Account ID: $CLOUDFLARE_ACCOUNT_ID"
fi

export CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID

cd "$WORKER_DIR"
DEPLOY_LOG="$(mktemp)"
npx wrangler deploy 2>&1 | tee "$DEPLOY_LOG"

URL="$(grep -oE 'https://muxtext-bug-pipeline\.[a-zA-Z0-9.-]+\.workers\.dev' "$DEPLOY_LOG" | head -1 || true)"
if [[ -z "$URL" ]]; then
  URL="$(grep -oE 'https://[a-zA-Z0-9.-]+\.workers\.dev' "$DEPLOY_LOG" | grep muxtext-bug-pipeline | head -1 || true)"
fi
rm -f "$DEPLOY_LOG"

if [[ -z "$URL" ]]; then
  echo "Deploy finished but could not parse workers.dev URL."
  exit 1
fi

echo ""
echo "Bug pipeline worker URL: $URL"

python3 - "$URL" "$INDEX" <<'PY'
import re, sys
url, path = sys.argv[1], sys.argv[2]
text = open(path, encoding='utf-8').read()
new = re.sub(
    r"BUG_PIPELINE_CONFIG=\{endpoint:'[^']*',pollIntervalMs:(\d+),reportCooldownMs:(\d+)\}",
    f"BUG_PIPELINE_CONFIG={{endpoint:'{url}',pollIntervalMs:\\1,reportCooldownMs:\\2}}",
    text,
    count=1,
)
if new == text:
    print(f'BUG_PIPELINE_CONFIG.endpoint already set to {url}')
else:
    open(path, 'w', encoding='utf-8').write(new)
    print(f'Updated BUG_PIPELINE_CONFIG.endpoint in {path}')
PY

echo ""
echo "Verify: curl -sS '$URL/health'"
