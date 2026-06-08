#!/usr/bin/env bash
# Deploy muxtext-bug-pipeline Worker and write workers.dev URL into index.html.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORKER_DIR="$ROOT/workers/bug-pipeline"
INDEX="$ROOT/index.html"

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]] || [[ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]]; then
  echo "Missing Cloudflare credentials."
  echo ""
  echo "Required env vars:"
  echo "  CLOUDFLARE_API_TOKEN   — https://dash.cloudflare.com/profile/api-tokens"
  echo "                         (Workers Scripts Edit + Durable Objects Edit)"
  echo "  CLOUDFLARE_ACCOUNT_ID  — Cloudflare dashboard → right sidebar"
  echo ""
  echo "GitHub Actions: repo Settings → Secrets → Actions → add both secrets,"
  echo "then Actions → Deploy Bug Pipeline Worker → Run workflow."
  exit 1
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
