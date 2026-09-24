#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DIR="$ROOT/mcp/wikipedia/Ravishka17-Wikipedia-MCP"

if [[ ! -d "$DIR" ]]; then
  git clone https://github.com/Ravishka17/Wikipedia-MCP.git "$DIR"
fi

cd "$DIR"
npm install
npm run build
exec npm start
