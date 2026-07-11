# Ghostfeed Agent Skills

Skills that teach AI agents how to drive [Ghostfeed](https://ghostfeed.ai) well over MCP. Each skill is a plain `SKILL.md` following the [Agent Skills spec](https://agentskills.io); the content is generated into the [Ghostfeed docs](https://ghostfeed.ai/docs) from the same source.

## Install

```bash
npx skills add ghostfeed-ai/skills --skill ghostfeed-avatars
```

The [skills CLI](https://github.com/vercel-labs/skills) installs into whichever agents you use (Claude Code, Cursor, Codex, and others). No Node? Fetch the raw file:

```bash
mkdir -p ~/.claude/skills/ghostfeed-avatars
curl -o ~/.claude/skills/ghostfeed-avatars/SKILL.md https://ghostfeed.ai/skills/ghostfeed-avatars.md
```

## Skills

- `ghostfeed-avatars`: the avatar create/approve flow: traits vs scene, agent-picked names, draft approval, the money line.

Connect the Ghostfeed MCP server first: see the [quickstart](https://ghostfeed.ai/docs).
