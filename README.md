# Robynn plugins for Claude Code

This repository is a Claude Code plugin marketplace named `robynn`.

| Plugin | What it does |
|---|---|
| [`memory-vault`](plugins/memory-vault) | Saves your Claude Code sessions to [Memory Vault](https://memory.robynn.ai) as you work: each prompt and Claude's final reply, never files or tool output. |

Add it in Claude (claude.ai or the Claude app): open **Customize**, then **Plugins**, choose **Add marketplace**, and enter `robynnai/claude-plugins`. Or, in Claude Code:

```
/plugin marketplace add robynnai/claude-plugins
/plugin install memory-vault@robynn
```

Read [the plugin's README](plugins/memory-vault/README.md) for exactly what it sends and how to turn it off.

Maintainers: [docs/PUBLISHING.md](docs/PUBLISHING.md) and [docs/TEST_PLAN.md](docs/TEST_PLAN.md).
