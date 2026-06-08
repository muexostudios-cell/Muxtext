#!/usr/bin/env bash
# Auto-resolve Cloudflare Account ID from API token, deploy workers, patch index.html,
# and optionally push secrets to GitHub Actions.
#
# Usage (minimal — only paste API token once):
#   CLOUDFLARE_API_TOKEN=your_token bash tools/setup-cloudflare-auto.sh
#
# Or interactive:
#   bash tools/setup-cloudflare-auto.sh
#
# Wrangler OAuth (click link in terminal; works when callback reaches this machine):
#   bash tools/setup-cloudflare-auto.sh --wrangler-login
#
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO="${GITHUB_REPOSITORY:-muexostudios-cell/Muxtext}"
CF_API="https://api.cloudflare.com/client/v4"
WRANGLER_LOGIN=false
DEPLOY_BUG=true
SET_GH_SECRETS=true
COMMIT_INDEX=true

usage() {
  sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage 0 ;;
    --wrangler-login) WRANGLER_LOGIN=true; shift ;;
    --no-gh-secrets) SET_GH_SECRETS=false; shift ;;
    --no-commit) COMMIT_INDEX=false; shift ;;
    --token)
      CLOUDFLARE_API_TOKEN="${2:-}"
      shift 2
      ;;
    *) echo "Unknown option: $1" >&2; usage 1 ;;
  esac
done

need_jq() {
  command -v jq >/dev/null 2>&1 || { echo "Installing jq..."; sudo apt-get update -qq && sudo apt-get install -y -qq jq; }
}

cf_curl() {
  curl -sS -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" -H "Content-Type: application/json" "$@"
}

verify_api_token() {
  local resp
  resp="$(cf_curl "${CF_API}/user/tokens/verify")"
  echo "$resp" | jq -e '.success == true and .result.status == "active"' >/dev/null
  echo "Token valid (id=$(echo "$resp" | jq -r '.result.id'))"
}

resolve_account_id() {
  local resp pick
  resp="$(cf_curl "${CF_API}/accounts?per_page=50")"
  if ! echo "$resp" | jq -e '.success == true' >/dev/null; then
    echo "Failed to list accounts:" >&2
    echo "$resp" | jq . >&2 || echo "$resp" >&2
    exit 1
  fi
  pick="$(echo "$resp" | jq -r '.result[] | select(.name|test("muexo";"i")) | .id' | head -1)"
  if [[ -z "$pick" ]]; then
    pick="$(echo "$resp" | jq -r '.result[0].id // empty')"
  fi
  if [[ -z "$pick" ]]; then
    echo "No Cloudflare accounts found for this token." >&2
    exit 1
  fi
  local name
  name="$(echo "$resp" | jq -r --arg id "$pick" '.result[] | select(.id==$id) | .name')"
  echo "Account: $name ($pick)"
  CLOUDFLARE_ACCOUNT_ID="$pick"
  export CLOUDFLARE_ACCOUNT_ID
}

try_wrangler_login() {
  echo ""
  echo "=== Wrangler OAuth login ==="
  echo "If this VM cannot receive localhost:8976 callbacks, use API token mode instead:"
  echo "  CLOUDFLARE_API_TOKEN=... bash tools/setup-cloudflare-auto.sh"
  echo ""
  local login_log
  login_log="$(mktemp)"
  printf 'n\n' | npx wrangler login --browser false --install-skills false 2>&1 | tee "$login_log" &
  local login_pid=$!
  local deadline=$((SECONDS + 300))
  while (( SECONDS < deadline )); do
    if npx wrangler whoami --json 2>/dev/null | jq -e '.accounts[0].id' >/dev/null 2>&1; then
      kill "$login_pid" 2>/dev/null || true
      wait "$login_pid" 2>/dev/null || true
      rm -f "$login_log"
      return 0
    fi
    if ! kill -0 "$login_pid" 2>/dev/null; then
      break
    fi
    sleep 3
  done
  kill "$login_pid" 2>/dev/null || true
  wait "$login_pid" 2>/dev/null || true
  if grep -q 'Visit this link' "$login_log" 2>/dev/null; then
    echo ""
    grep 'Visit this link' "$login_log" | sed 's/Visit this link to authenticate: //'
    echo ""
    echo "Open the link above, authorize, then re-run with your API token if OAuth callback fails."
  fi
  rm -f "$login_log"
  return 1
}

extract_token_from_wrangler() {
  local whoami
  whoami="$(npx wrangler whoami --json 2>/dev/null || true)"
  if [[ -z "$whoami" ]]; then
    return 1
  fi
  CLOUDFLARE_ACCOUNT_ID="$(echo "$whoami" | jq -r '.accounts[0].id // empty')"
  echo "Wrangler account: $(echo "$whoami" | jq -r '.accounts[0].name // "?"') ($CLOUDFLARE_ACCOUNT_ID)"
  # Wrangler OAuth is not the same as API token — still need API token for gh secrets
  if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
    echo ""
    echo "Wrangler login OK. Create an API token and re-run:"
    echo "  https://dash.cloudflare.com/profile/api-tokens → Edit Cloudflare Workers"
    echo "  CLOUDFLARE_API_TOKEN=... bash tools/setup-cloudflare-auto.sh"
    exit 0
  fi
  export CLOUDFLARE_ACCOUNT_ID
}

prompt_token() {
  if [[ -n "${CLOUDFLARE_API_TOKEN:-}" ]]; then
    return 0
  fi
  echo ""
  echo "Paste Cloudflare API Token (input hidden), then Enter:"
  echo "Create at: https://dash.cloudflare.com/profile/api-tokens"
  echo "Template: Edit Cloudflare Workers (Workers Scripts + Durable Objects Edit)"
  read -rs CLOUDFLARE_API_TOKEN
  echo ""
  export CLOUDFLARE_API_TOKEN
  if [[ -z "$CLOUDFLARE_API_TOKEN" ]]; then
    echo "No token provided." >&2
    exit 1
  fi
}

set_github_secrets() {
  if [[ "$SET_GH_SECRETS" != true ]]; then
    return 0
  fi
  if ! command -v gh >/dev/null 2>&1; then
    echo "::warning::gh CLI not found — skip GitHub secrets"
    return 0
  fi
  if ! gh auth status >/dev/null 2>&1; then
    echo "::warning::gh not authenticated — skip GitHub secrets"
    return 0
  fi
  echo "Setting GitHub Actions secrets on $REPO ..."
  if gh secret set CLOUDFLARE_API_TOKEN -R "$REPO" -b"$CLOUDFLARE_API_TOKEN" 2>/dev/null; then
    echo "  CLOUDFLARE_API_TOKEN ✓"
  else
    echo "::warning::Could not set CLOUDFLARE_API_TOKEN (need repo admin)"
  fi
  if gh secret set CLOUDFLARE_ACCOUNT_ID -R "$REPO" -b"$CLOUDFLARE_ACCOUNT_ID" 2>/dev/null; then
    echo "  CLOUDFLARE_ACCOUNT_ID ✓"
  else
    echo "::warning::Could not set CLOUDFLARE_ACCOUNT_ID (need repo admin)"
  fi
}

deploy_and_patch() {
  export CLOUDFLARE_API_TOKEN CLOUDFLARE_ACCOUNT_ID
  if [[ "$DEPLOY_BUG" == true ]]; then
    bash "$ROOT/tools/deploy-bug-pipeline-worker.sh"
  fi
}

commit_index_if_changed() {
  if [[ "$COMMIT_INDEX" != true ]]; then
    return 0
  fi
  cd "$ROOT"
  if git diff --quiet index.html 2>/dev/null; then
    return 0
  fi
  git add index.html
  git commit -m "chore: set BUG_PIPELINE_CONFIG.endpoint after Cloudflare deploy"
  if git push origin HEAD 2>/dev/null; then
    echo "Pushed index.html with bug pipeline endpoint."
  else
    echo "::warning::Commit created locally; push manually."
  fi
}

trigger_workflow() {
  if ! command -v gh >/dev/null 2>&1; then
    return 0
  fi
  gh workflow run deploy-bug-pipeline-worker.yml -R "$REPO" 2>/dev/null && \
    echo "Triggered Deploy Bug Pipeline Worker workflow." || true
}

main() {
  need_jq
  cd "$ROOT"

  if [[ "$WRANGLER_LOGIN" == true ]]; then
    try_wrangler_login || true
    extract_token_from_wrangler || true
  fi

  prompt_token
  verify_api_token
  resolve_account_id
  set_github_secrets
  deploy_and_patch
  commit_index_if_changed
  trigger_workflow

  echo ""
  echo "Done."
  echo "  Account ID : $CLOUDFLARE_ACCOUNT_ID"
  echo "  Verify     : curl -sS \$(grep -oP \"BUG_PIPELINE_CONFIG=\\{endpoint:'\\K[^']+\" index.html)/health"
}

main "$@"
