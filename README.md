# Ghostfeed Skills: AI Agent Skills for UGC Videos, AI Avatars, and TikTok Slideshows

Teach your AI agent to run a full UGC content pipeline. These skills give Claude Code, Cursor, Codex, Grok Build, and 70+ other agents the product knowledge to create AI avatars, generate UGC reaction videos, and build TikTok photo slideshows through the [Ghostfeed](https://ghostfeed.ai) MCP server, with the same guardrails the Ghostfeed dashboard enforces.

<a href="https://ghostfeed.ai"><img src="./media/demo.webp" width="100%" alt="Grid of AI UGC avatars, men and women, all generated with Ghostfeed" /></a>

[![Agent Skills spec](https://img.shields.io/badge/format-Agent_Skills_spec-blue)](https://agentskills.io)
[![Works with 70+ agents](https://img.shields.io/badge/works_with-70%2B_agents-brightgreen)](https://github.com/vercel-labs/skills)
[![Ghostfeed docs](https://img.shields.io/badge/docs-ghostfeed.ai-orange)](https://ghostfeed.ai/docs)

## What's inside

Each skill is a plain `SKILL.md` following the [Agent Skills spec](https://agentskills.io), distilled from real founder dogfooding of the live product.

| Skill | What your agent learns |
| --- | --- |
| [`ghostfeed-avatars`](https://ghostfeed.ai/docs/skills/ghostfeed-avatars) | Create AI avatar drafts from appearance traits, review them with the user, and approve selected identities into the library. Nothing is approved or spent without an explicit user decision. |
| [`ghostfeed-ugc-reactions`](https://ghostfeed.ai/docs/skills/ghostfeed-ugc-reactions) | Produce UGC reaction videos the way the dashboard does: pick a source template, render the avatar into the opening pose, get the first frame approved, then animate it by cloning the reference motion or directing it with a prompt. |
| [`ghostfeed-slideshows`](https://ghostfeed.ai/docs/skills/ghostfeed-slideshows) | Art-direct TikTok photo slideshows end to end: start a blank deck, cast every background image, write the on-image text, review, and hand back the link. |

## Install

Install every Ghostfeed skill, then choose your agents and scope at the prompt:

```bash
npx skills add ghostfeed-ai/skills --skill '*'
```

The wildcard selects the complete bundle. Global installs land in the shared `~/.agents/skills/` directory that Claude Code, Codex, Cursor, Grok Build, and the rest of the [skills CLI](https://github.com/vercel-labs/skills) agents read.

No Node? Download the complete bundle:

```bash
curl -LsS https://api.github.com/repos/ghostfeed-ai/skills/tarball/main \
  -o ghostfeed-skills.tar.gz
```

## Pair with the Ghostfeed MCP server

Skills describe the workflow; the [Ghostfeed agent platform](https://ghostfeed.ai/docs) does the work. One URL, OAuth in the browser, no API keys:

```
https://api.ghostfeed.ai/api/v2/mcp
```

Setup guides for Claude Code, Claude apps, ChatGPT, Cursor, VS Code, Codex, Grok, and any other MCP client live in the [quickstart](https://ghostfeed.ai/docs). In Claude apps and ChatGPT the server also renders interactive widgets in the chat: an avatar builder, a video crop editor, media galleries, and playable results.

## Why skills instead of a long prompt

A skill captures the judgment a good operator applies: which tool to call first, what must be user-approved before money is spent, which failure modes to expect, and how to report results. Installing it once beats pasting instructions into every conversation, and the same skill file works across every agent the skills CLI supports.

## Links

- [Ghostfeed](https://ghostfeed.ai): AI UGC videos, avatars, and slideshows for TikTok and Reels
- [Documentation and quickstart](https://ghostfeed.ai/docs)
- [Agent API reference](https://ghostfeed.ai/docs/reference/avatars)
- [Agent Skills specification](https://agentskills.io)
- [skills CLI](https://github.com/vercel-labs/skills)
