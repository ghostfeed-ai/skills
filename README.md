# Ghostfeed Agent Skills

Skills that teach AI agents how to drive [Ghostfeed](https://ghostfeed.ai) well over MCP. Each skill
is a plain `SKILL.md` following the [Agent Skills spec](https://agentskills.io). The
[Ghostfeed docs](https://ghostfeed.ai/docs) and this install repository are published from the same
source.

## Install

Install every Ghostfeed skill, then choose your agents and scope at the prompt:

```bash
npx skills add ghostfeed-ai/skills --skill '*'
```

The wildcard selects the complete bundle. The
[skills CLI](https://github.com/vercel-labs/skills) installs it for Claude Code, Cursor, Codex, and
other supported agents.

No Node? Download the complete bundle:

```bash
curl -LsS https://api.github.com/repos/ghostfeed-ai/skills/tarball/main \
  -o ghostfeed-skills.tar.gz
```

## Skills

- `ghostfeed-avatars`: create avatar drafts, review them, and approve selected identities.
- `ghostfeed-slideshows`: create or remix photo slideshows, follow generation, and review the deck.
- `ghostfeed-ugc-reactions`: import a source clip, render an avatar into its first frame, get that
  frame approved, then animate it by cloning the reference motion or from a prompt.

Connect the Ghostfeed MCP server first: see the [quickstart](https://ghostfeed.ai/docs).
