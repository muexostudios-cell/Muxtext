#!/usr/bin/env bash
# Deploy muxtext-chat Worker and write the live workers.dev URL into index.html.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHAT_DIR="$ROOT/workers/chat"
INDEX="$ROOT/index.html"

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  echo "Missing CLOUDFLARE_API_TOKEN."
  echo "Create at: https://dash.cloudflare.com/profile/api-tokens"
  echo "Required permissions: Account / Workers Scripts / Edit, Durable Objects / Edit"
  exit 1
fi

cd "$CHAT_DIR"
DEPLOY_LOG="$(mktemp)"
npx wrangler deploy 2>&1 | tee "$DEPLOY_LOG"

URL="$(grep -oE 'https://muxtext-chat\.[a-zA-Z0-9.-]+\.workers\.dev' "$DEPLOY_LOG" | head -1 || true)"
if [[ -z "$URL" ]]; then
  URL="$(grep -oE 'https://[a-zA-Z0-9.-]+\.workers\.dev' "$DEPLOY_LOG" | grep muxtext-chat | head -1 || true)"
fi

rm -f "$DEPLOY_LOG"

if [[ -z "$URL" ]]; then
  echo ""
  echo "Deploy finished but could not parse workers.dev URL from wrangler output."
  echo "Check Cloudflare dashboard → Workers → muxtext-chat"
  exit 1
fi

echo ""
echo "Chat worker URL: $URL"

python3 - "$URL" "$INDEX" <<'PY'
import re, sys
url, path = sys.argv[1], sys.argv[2]
text = open(path, encoding='utf-8').read()
new = re.sub(
    r"CHAT_CONFIG=\{endpoint:'[^']*',pollIntervalMs:(\d+)\}",
    f"CHAT_CONFIG={{endpoint:'{url}',pollIntervalMs:\\1}}",
    text,
    count=1,
)
if new == text:
    raise SystemExit('Could not update CHAT_CONFIG.endpoint in index.html')
open(path, 'w', encoding='utf-8').write(new)
print(f'Updated CHAT_CONFIG.endpoint in {path}')
PY

echo ""
echo "Verify: curl -sS '$URL/health'"
