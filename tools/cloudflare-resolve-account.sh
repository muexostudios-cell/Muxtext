#!/usr/bin/env bash
# Resolve CLOUDFLARE_ACCOUNT_ID from CLOUDFLARE_API_TOKEN (for CI / local deploy).
set -euo pipefail

if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
  echo "CLOUDFLARE_API_TOKEN is required" >&2
  exit 1
fi

resp="$(curl -sS -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/accounts?per_page=50")"

if ! command -v jq >/dev/null 2>&1; then
  echo "$resp" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if not d.get('success'): sys.exit(1)
accs=d.get('result') or []
pick=next((a['id'] for a in accs if 'muexo' in a.get('name','').lower()), None)
print(pick or (accs[0]['id'] if accs else ''))
"
else
  echo "$resp" | jq -r '
    (.result[] | select(.name|test("muexo";"i")) | .id) // .result[0].id // empty
  ' | head -1
fi
