---
name: ghostfeed-avatars
description: Drive Ghostfeed's avatar create/approve flow over MCP. Gather intent, generate drafts, let the user approve. Refined from real testing.
---

The tools enforce the hard rules server-side: drafts are never auto-saved,
traits are validated, every op is workspace-scoped, failed generations refund.
This skill shapes the conversation on top.

## The flow

1. Split identity from scene. Persistent identity goes in `traits` (gender,
   ageBand, heritage, faceShape, skinTone, skinTexture, hairColor, hairStyle,
   eyeColor, bodyBuild, outfitStyle). This-shot scene, pose, mood, and
   lighting go in `notes`. Omitted traits are randomized (gender-aware), so
   pass only what the user specified.
2. Name them yourself. Pick trait-appropriate `names` (one per draft); the
   server's auto-namer is trait-blind and once named an East Asian avatar
   "Luis Iqbal". Call `create_avatar` (`count` up to 4). If the user asks
   about quality or model options, call `list_image_models` and show the
   choices with per-image prices; otherwise the default model is fine.
3. Present the drafts. Every draft in the result has a public `imageUrl` that
   opens in any browser. Render each one: `![Name](imageUrl)` where the
   client shows inline images (claude.ai), `[Name](imageUrl)` as a clickable
   link in terminal clients.
4. The user chooses. Never approve or delete on their behalf.
   `approve_avatar(avatarId)` for keepers, `delete_draft_avatar(avatarId)` for
   the rest, `rename_avatar(avatarId, name)` for a name change.
5. Drafts persist across sessions. If `list_draft_avatars` shows old
   unapproved ones, tell the user.

## Discovering options and ids

Trait fields are enums. Read them off the tool schema and offer them:
"heritage can be South Asian, East Asian, Black, White, Latino, Middle
Eastern, or Mixed." A wrong value returns `validation_failed` with the allowed
list; correct and retry.

To find a saved avatar's id (rename, content generation), use `list_avatars`.
Never guess ids; never scrape the dashboard.

## Money

`create_avatar` returns `creditsSpent` and `creditsRemaining`. Failures refund
automatically; a partial batch refunds the undelivered images.

End the reply with the money on its own line, numbers from the tool result:

```
💳 {creditsSpent} credits spent, {creditsRemaining} remaining
```

Free operations (approve, rename, delete, lists) get no money line.
