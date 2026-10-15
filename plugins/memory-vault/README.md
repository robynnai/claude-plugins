# Robynn Memory Vault for Claude Code

Saves your Claude Code sessions to [Memory Vault](https://memory.robynn.ai) as you work, so ChatGPT, Claude, Codex and your other AI apps can pick up where you left off. No terminal and no command-line tool.

## Set up

1. **Add the plugin.**
   - In Claude (claude.ai or the Claude app): open **Customize**, then **Plugins**, choose **Add marketplace**, enter `robynnai/claude-plugins`, and turn on **Robynn Memory Vault**. It reaches Claude Code on every computer where you sign in with the same Claude account (Claude Code 2.1.273 or later).
   - Or, in Claude Code: `/plugin marketplace add robynnai/claude-plugins`, then `/plugin install memory-vault@robynn`.
2. **Sign in once on each computer.** In Claude Code, run `/mcp`, choose `plugin:memory-vault:session-sync`, and sign in with your Memory Vault account. The sign-in page asks you to allow **Memory Vault importer**.

Until you sign in, Claude Code shows that a server needs sign-in, notes a hook error after each prompt and reply, and saves nothing.

## What it sends, and where

While the plugin is on and you're signed in, Claude Code sends the following to Memory Vault (`mcp.memory.robynn.ai`, run by Robynn AI). It goes over HTTPS, signed in as you:

| When | What |
|---|---|
| You send a prompt | The text of your prompt |
| Claude finishes replying | The text of Claude's final reply to that prompt |
| Each time | Claude Code's session ID and prompt ID, so nothing is saved twice, and the folder you're working in with your home folder shortened to `~` (for example `~/code/site`) |

**It never sends:**

- your files or their contents
- tool calls or their results: the commands Claude runs, their output, diffs, search results and web pages
- the text Claude writes between tool calls
- images or attachments
- your settings, environment variables or credentials
- sessions from before you installed it

**What Memory Vault does with it:**

- It removes likely passwords, API keys and tokens before storing anything.
- It keeps each session as a conversation in your personal memory, which only you and the apps you allow can see.
- An AI model writes a short handoff for each session (goal, where the work stands, next step) so your other apps can continue it. On the Free plan, handoffs count toward your monthly allowance.
- If Memory Vault for Mac or the command-line importer also saves a session, its full transcript replaces what the plugin saved.

**What runs on your computer.** This plugin includes no program. Claude Code itself sends the prompt and reply, through the plugin's Memory Vault connection (`mcp_tool` hooks in `hooks/hooks.json`). The only script is `hooks/first-run.sh`, which shows a setup message once per computer and reads or sends nothing.

Privacy policy: <https://robynn.ai/privacy>

## Turn it off

- **On this computer:** `/plugin`, then Installed, then memory-vault, then Disable (or `claude plugin disable memory-vault@robynn`).
- **Everywhere:** in Claude's **Customize**, then **Plugins**, turn off Robynn Memory Vault.
- **For your whole account:** in Memory Vault, open Connected apps and revoke **Memory Vault importer**. This also stops the command-line importer.
- **Sign out on one computer:** `/mcp`, then `plugin:memory-vault:session-sync`, then clear its authentication.
- **Delete what's saved:** delete the conversation in Memory Vault. A deleted conversation isn't saved again.

## Past sessions

The plugin saves sessions from the moment you sign in. To bring in older ones, sign in to Memory Vault, then go to **Add to memory**, **AI apps**, then **Claude Code**, and use the command shown there (it needs a terminal). Memory Vault for Mac does the same on a Mac without one.

## Help

<https://memory.robynn.ai/desktop-help#claude-code> · support@robynn.ai
