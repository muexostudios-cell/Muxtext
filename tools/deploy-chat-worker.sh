#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../workers/chat"
npx wrangler deploy
echo ""
echo "Set CHAT_CONFIG.endpoint in index.html to your workers.dev URL, e.g.:"
echo "  https://muxtext-chat.<your-subdomain>.workers.dev"
