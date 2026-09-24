#!/usr/bin/env bash
set -euo pipefail

# Wikipedia / MediaWiki MCP stack for Codex.
# This script is intentionally secret-free: credentials belong in the runtime,
# never in this repository.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONFIG="$ROOT/mcp/wikipedia/config.json"

ensure_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

ensure_cmd codex
ensure_cmd pipx
ensure_cmd npx

echo "Ensuring Rudra-ravi Wikipedia MCP is installed..."
if pipx list 2>/dev/null | grep -q "wikipedia-mcp"; then
  pipx upgrade wikipedia-mcp >/dev/null || true
else
  pipx install wikipedia-mcp
fi

ensure_mcp_stdio() {
  local name="$1"
  shift
  if codex mcp list | awk '{print $1}' | grep -qx "$name"; then
    echo "MCP already registered: $name"
  else
    "$@"
  fi
}

echo "Registering ProfessionalWiki MediaWiki MCP..."
ensure_mcp_stdio mediawiki codex mcp add mediawiki \
  --env CONFIG="$CONFIG" \
  -- npx -y @professional-wiki/mediawiki-mcp-server@latest

echo "Registering Rudra-ravi Wikipedia MCP..."
ensure_mcp_stdio wikipedia codex mcp add wikipedia -- \
  wikipedia-mcp --language en --enable-cache

if [[ -n "${RAVISHKA_MCP_URL:-}" ]]; then
  echo "Registering Ravishka17 cross-check MCP..."
  if codex mcp list | awk '{print $1}' | grep -qx "wikipedia-crosscheck"; then
    echo "MCP already registered: wikipedia-crosscheck"
  else
    codex mcp add wikipedia-crosscheck --transport http "$RAVISHKA_MCP_URL"
  fi
else
  echo "RAVISHKA_MCP_URL not set; cross-check server not registered."
  echo "Set it to a reachable Streamable HTTP endpoint before running a 3-source iteration."
fi

echo
echo "Registered MCP servers:"
codex mcp list
