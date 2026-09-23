#!/usr/bin/env bash
set -euo pipefail

# Wikipedia / MediaWiki MCP stack for Codex.
# Run this script from a machine where Codex CLI, Node/npx and pipx are installed.

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$ROOT/mcp/wikipedia/config.json"

echo "Installing Rudra-ravi Wikipedia MCP..."
pipx install wikipedia-mcp

echo "Registering ProfessionalWiki MediaWiki MCP..."
codex mcp add mediawiki \
  --env CONFIG="$CONFIG" \
  -- npx -y @professional-wiki/mediawiki-mcp-server@latest

echo "Registering Rudra-ravi Wikipedia MCP..."
codex mcp add wikipedia -- \
  wikipedia-mcp --language en --enable-cache

# Optional independent HTTP cross-check server.
# Set RAVISHKA_MCP_URL only after deploying your own Ravishka17 server.
if [[ -n "${RAVISHKA_MCP_URL:-}" ]]; then
  echo "Registering Ravishka17 cross-check MCP..."
  codex mcp add wikipedia-crosscheck --transport http "$RAVISHKA_MCP_URL"
else
  echo "RAVISHKA_MCP_URL not set; cross-check server not registered."
fi

echo
echo "Registered MCP servers:"
codex mcp list
