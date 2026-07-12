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
   pass only what the user specified; when the brief has a register (brand
   ad, editorial), also set skinTexture and makeupStyle to match, because the
   dice do not read the brief. `notes` is a light vibe hint, not a scene
   contract: at creation the engine owns the scene, since these images are
   identity/base material and exact scenes are generated later from the
   avatar page. To iterate on a draft ("same person, but X"), copy the
   `traits` object echoed in the previous result and change only what the
   user asked; anything omitted re-randomizes on every call.
2. Name them yourself. Pick trait-appropriate `names` (one per draft); the
   server's auto-namer is trait-blind and once named an East Asian avatar
   "Luis Iqbal". Call `create_avatar` (`count` up to 4). `count` makes look
   variations of ONE trait spec, not different people; for distinct personas
   make one call each. If the user asks about quality or model options, call
   `list_image_models` and show the choices with per-image prices; otherwise
   the default model is fine.
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

Workspace-scoped tools take an optional `workspace` (an id or exact name
from `list_workspaces`) to act in a specific workspace; omit it to use the
connection's default. If two workspaces share a name the error lists the
ids; retry with the id.

## Money

`create_avatar` returns `creditsSpent` and `creditsRemaining`. Failures refund
automatically; a partial batch refunds the undelivered images. Creation bills
once: drafts never expire and cost nothing to keep. The balance is a shared
pool that teammates can move between your calls; `list_transactions` with
`mine: true` shows exactly what this connection spent.

End the reply with the money on its own line, numbers from the tool result:

```
💳 {creditsSpent} credits spent, {creditsRemaining} remaining
```

Free operations (approve, rename, delete, lists) get no money line.
