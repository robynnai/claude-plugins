#!/bin/bash
# Once per computer: tell the person how to finish setting up. Reads and sends nothing.
# Hooks can't start a sign-in, so until they sign in from /mcp nothing is saved.
marker="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/plugins/data/memory-vault}/welcomed"
[ -e "$marker" ] && exit 0
mkdir -p "$(dirname "$marker")" 2>/dev/null && : > "$marker" 2>/dev/null
printf '%s\n' '{"systemMessage": "Memory Vault is installed. To start saving this computer'"'"'s Claude Code sessions, run /mcp, choose plugin:memory-vault:session-sync and sign in. It saves each prompt and Claude'"'"'s final reply, never files or tool output. To stop, disable the plugin in /plugin."}'
exit 0
