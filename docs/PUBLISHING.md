# Publishing the Robynn marketplace

Nothing here is public yet. Publishing needs the owner's approval for each step below.

## Order

1. **Server first.** The `gc_session_save` MCP tool must be live on the server the plugin points at (growth-cortex PR "Claude Code plugin: save sessions live"). Until then, every hook call fails with an unknown-tool error.
2. **Repository.** Create the GitHub repository for this marketplace and push `main`.
   - It must be **public**. claude.ai's Add marketplace documents github.com repositories, and public GitLab and Bitbucket ones. Private repositories aren't documented for personal accounts. Organization sync needs a private or internal repo.
   - Suggested name: `robynnai/claude-plugins`. Any name works; the marketplace is called `robynn` either way.
3. **Fill in the address.** Replace `ROBYNN_MARKETPLACE_REPO` in `README.md` and `plugins/memory-vault/README.md` with the repository (`owner/repo`).
4. **Turn on the web offer.** Set `GC_CLAUDE_CODE_PLUGIN_MARKETPLACE=<owner/repo>` in Doppler `prd_gc_web`, apply it with `scripts/gc_fly_secrets.sh prd web`, then `fly secrets deploy -a growth-cortex-web`. The web app's Claude Code card and `/desktop-help#claude-code` then show the plugin.
5. **Try it from a clean account** (docs/TEST_PLAN.md, the "Synced" cases).

## Versions

`plugin.json` sets `version`, so installed copies update only when it changes. Bump it for every user-visible change and tag the release (`claude plugin tag plugins/memory-vault`).

## Directory listing: no

Anthropic's Software Directory Policy forbids extracting chat history, so this plugin is distributed only through this marketplace. It must not be submitted to Anthropic's plugin directory.

## Staging and local copies

`scripts/variant.py <out-dir> <mcp-origin> [client-id]` writes a copy pointed at another server. For example:

```bash
scripts/variant.py /tmp/mv-staging https://growth-cortex-staging.fly.dev
claude --plugin-dir /tmp/mv-staging
```

The copy keeps the name `memory-vault`. Don't load it in the same session as an installed production copy.
