# Test plan: memory-vault plugin

The server side (`gc_session_save`, transcript replacement, tool visibility) has automated tests in growth-cortex: `tests/gc_threads/test_live_turns.py` and `tests/gc_transport/test_threads_mcp.py`. This plan covers the plugin in Claude Code.

## Setup

- **Claude Code:** 2.1.273 or later (synced plugins). Record the version under test (`claude --version`).
- **Local:** run the API from a growth-cortex checkout with `GC_REPO=<checkout> gc-api-local.sh 8010`, which uses staging sign-in. Then make a local copy of the plugin and start Claude Code with it:
  - `scripts/variant.py /tmp/mv-local http://127.0.0.1:8010 https://growth-cortex-staging.fly.dev/cli/client.json`
  - `claude --plugin-dir /tmp/mv-local`
- **Staging:** `scripts/variant.py /tmp/mv-staging https://growth-cortex-staging.fly.dev`. This needs the server PR deployed to staging.
- **Checks:** to confirm what reached the server, query the local database, or open Conversations in the web app on the same account.

## Static

| # | Check | Expect |
|---|---|---|
| S1 | `claude plugin validate .` and `claude plugin validate plugins/memory-vault --strict` | Both pass |
| S2 | `bash plugins/memory-vault/hooks/first-run.sh`, run twice with `CLAUDE_PLUGIN_DATA` set to a temp folder | First run prints one JSON `systemMessage`; the second prints nothing |

## Signed out

| # | Steps | Expect |
|---|---|---|
| A1 | Start Claude Code with the plugin, never signed in | Startup shows "1 MCP server needs authentication · run /mcp" and the one-time setup message |
| A2 | Send a prompt | Claude answers normally. A "UserPromptSubmit hook error … plugin:memory-vault:session-sync not connected" line appears, and a Stop hook error after the reply. Nothing reaches the server |
| A3 | Restart Claude Code | No setup message the second time (once per computer) |

## Sign-in

| # | Steps | Expect |
|---|---|---|
| B1 | `/mcp`, choose `plugin:memory-vault:session-sync`, Authenticate | The browser opens the AuthKit sign-in. The client is "Memory Vault importer", with no dynamic registration. Return to Claude Code shows connected |
| B2 | `/mcp`, view the server | 0 tools. The system prompt carries no Memory Vault instructions |
| B3 | Web app, Connected apps | "Memory Vault importer" is active, adding conversations only |

## Saving

| # | Steps | Expect |
|---|---|---|
| C1 | Two prompts in a new session | One Claude Code conversation, titled from the first prompt, with project `~/…` and 4 messages (user, assistant, user, assistant). The Claude Code tile reads "Saving new chats" |
| C2 | A prompt that makes Claude edit a file and run a command | Only the prompt and the final reply are stored. No file content, diff, command or command output |
| C3 | `/exit`, then wait 10 minutes | Nothing is sent at exit and no hook error shows (the plugin has no SessionEnd hook: Claude Code 2.1.296 gives an interactive SessionEnd hook no MCP connection). The handoff is written after 10 quiet minutes |
| C4 | `claude --resume` the same session, then one more prompt | Appended to the same conversation |
| C5 | A prompt containing `sk-ant-` followed by 30 characters | Stored as `[redacted]` |
| C6 | A prompt over 64 KB | Stored trimmed, ending in `[trimmed]` |
| C7 | Two Claude Code windows at once | Two conversations, each with its own messages |
| C8 | Slash commands (`/mcp`, `/plugin`) | Not stored |
| C9 | Another plugin's Stop hook sends Claude back to work | Both final replies are kept, no duplicates |

## Interplay

| # | Steps | Expect |
|---|---|---|
| D1 | Save a session with the plugin, then import it with the CLI (`growth-cortex import claude-code`) or the Mac app | The conversation now holds the full transcript (with tool trail lines). The plugin's turns are gone, and later plugin turns are not added |
| D2 | Delete the conversation in the web app, then keep chatting in that session | Nothing more is saved (status `deleted`). No hook error |
| D3 | Revoke "Memory Vault importer" in Connected apps, then send a prompt | A hook error says saving is turned off and names Connected apps. Reconnecting restores saving |
| D4 | Free plan account past its monthly handoffs | Messages are still saved. The handoff shows as paused for the plan |

## Failure

| # | Steps | Expect |
|---|---|---|
| E1 | Stop the API, then send a prompt | Claude Code waits at most 10 s, shows a hook error and answers normally |
| E2 | Disable the plugin (`/plugin`) | No hook runs. Nothing is sent |

## Synced from claude.ai (needs the published repository)

| # | Steps | Expect |
|---|---|---|
| F1 | claude.ai → Customize → Plugins → Add marketplace `<owner/repo>`, turn on Robynn Memory Vault | Listed in claude.ai |
| F2 | Start Claude Code (signed in with that claude.ai account) | The plugin appears as synced (`claude plugin list`). Its hooks and the `session-sync` server load. Sign-in is still needed per computer (B1) |
| F3 | Claude desktop app, Code tab | Same as F2. Check that `/mcp` sign-in works there |
| F4 | Turn the plugin off in claude.ai | Claude Code stops loading it at the next start |
| F5 | Claude Code signed in with an API key | Sync doesn't apply. `/plugin marketplace add` and `/plugin install` work instead |

## Platforms

| # | Steps | Expect |
|---|---|---|
| G1 | Windows (Git Bash) | `first-run.sh` runs. A cwd of `C:\Users\<name>\code\x` is stored as `~\code\x` |
| G2 | Linux | A cwd of `/home/<name>/x` is stored as `~/x` |
