---
name: ghostfeed-avatars
description: Drive Ghostfeed's avatar create/approve flow over MCP. Gather intent, generate drafts, let the user approve. Refined from real testing.
---

The tools enforce the hard rules server-side: drafts are never auto-saved,
traits are validated, every op is workspace-scoped, failed generations refund.
This skill shapes the conversation on top.

## The flow

1. Orient a new user in one short sentence before asking for details: Ghostfeed
   first creates identity drafts, the user chooses one, and exact scenes or
   performances come later. Split identity from scene. Persistent identity goes
   in `traits` (gender,
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
   "Luis Iqbal". Call `create_avatar` with the chosen `workspace` (`count` up
   to 4). `count` makes look
   variations of ONE trait spec, not different people; for distinct personas
   make one call each. Before generating, say which image model and resolution
   will be used. If the user did not choose, call `list_image_models`, identify
   the `isDefault` model, and say that is the default; add one short sentence
   that they can ask for another listed model. Do not dump the whole catalog
   unless they ask. If they want quality or model options, show the relevant
   choices with per-image prices.
3. Present the drafts per Delivering assets in chat below. Summarize what you
   made and hand over the dashboard link so the user can see the faces and
   pick (the link ritual below).
4. The user chooses. Never approve on their behalf. Pass the same
   `workspace` to `approve_avatar` or `rename_avatar`. You cannot delete drafts;
   the user manages or discards the ones they do not want from the dashboard.

## Discovering options and ids

Trait fields are enums. Read them off the tool schema and offer them:
"heritage can be South Asian, East Asian, Black, White, Latino, Middle
Eastern, or Mixed." A wrong value returns `validation_failed` with the allowed
list; correct and retry.

To find a saved avatar's id (rename, content generation), use `list_avatars`.
Never guess ids; never scrape the dashboard.

Call `list_workspaces` first and keep the chosen workspace slug or id. Reads
may omit `workspace` and use the credential's pinned read default. Every
workspace-scoped write requires `workspace`; never infer it from whichever
workspace the user last opened in the dashboard. If two workspaces share a
name, retry with the stable slug or id.

## Delivering assets in chat

You are in an MCP Apps host when the product you run in renders MCP widgets
inline in the chat: claude.ai and the ChatGPT app do; CLI and editor agents
(Claude Code, Cursor, Codex) do not. There, deliver drafts with
`render_image_results`, one avatar-draft item per image; the widget carries
Approve, Use, and Download. Open `render_avatar_builder` when the user wants
to design an avatar; never hand-build a custom UI. An Approve click arrives
as a structured user message: call `approve_avatar` for that avatar id only.

Anywhere else, the exact `dashboardUrl` is the delivery (the link ritual
below); never a generic workspace URL.

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

Free operations (approve, rename, lists) get no money line.

When a response carries `dashboardUrl`, end with the door on its own line
(after the money line if both apply), so the user can always click through
to what was made:

```
🔗 {dashboardUrl}
```

One link even for a batch: the keeper's, or the project's.
