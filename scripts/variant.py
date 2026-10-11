#!/usr/bin/env python3
"""Copy the memory-vault plugin, pointed at another Memory Vault server, for testing.

  scripts/variant.py <out-dir> <mcp-origin> [client-id]

  # Staging (its importer client document is published):
  scripts/variant.py /tmp/mv-staging https://growth-cortex-staging.fly.dev
  # A local API on :8010 started by gc_mcp_local.sh against staging sign-in, which trusts
  # staging's published importer document:
  scripts/variant.py /tmp/mv-local http://127.0.0.1:8010 \
      https://growth-cortex-staging.fly.dev/cli/client.json

Then: claude --plugin-dir <out-dir>. The copy keeps the plugin's name, so it shares the
sign-in of any other copy that points at the same URL.
"""

import json
import shutil
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent / "plugins" / "memory-vault"


def main(argv: list[str]) -> int:
    if len(argv) not in (3, 4):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    out, origin = Path(argv[1]), argv[2].rstrip("/")
    client_id = argv[3] if len(argv) == 4 else f"{origin}/cli/client.json"
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(PLUGIN, out)
    config = out / ".mcp.json"
    data = json.loads(config.read_text())
    server = data["mcpServers"]["session-sync"]
    server["url"], server["oauth"]["clientId"] = f"{origin}/mcp", client_id
    config.write_text(json.dumps(data, indent=2) + "\n")
    print(f"{out}: session-sync -> {server['url']} (client {client_id})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
