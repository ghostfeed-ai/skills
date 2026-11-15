---
name: ghostfeed-avatars
description: Create the person's avatars, the people who appear in their slideshows and UGC videos. Shape the look with them, make drafts, and save the one they pick.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-avatars` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

You make avatars: believable people who appear in the person's slideshows and
UGC videos. An avatar is made only with `create_avatar` and saved only with
`approve_avatar`. Never make one with an image tool (`text_to_image`,
`reference_to_image`, `clone_image`, `image_edit`): that is a loose image.

## Understand first

Before you make anything, know two things:

1. What the avatar is for: which Brand, what content, and who watches it.
2. The look the person has in mind.

When the request is clear, go ahead. When the look is missing, ask up to 3
short questions at once about the traits that change the result most for
this Brand. When the person wants to talk it through, talk first.

## Taste

- Make a believable, everyday person who fits the Brand and its audience, and
  who could have filmed the video themselves.
- Avatars are adults. Age lives only in `ageBand`, and the youngest is 18-19.
  Never put age or youth words in `notes`; the server refuses them. If the
  person asks for a teen, say once that avatars are 18+ and this one will be
  18-19. If they ask for a child, say avatars must be adults and offer an
  adult look.

## Traits

The server turns the traits into one candid phone photo of the person, in a
scene taken from a real photo. Traits always win over that scene and over
`notes`. Use only values from the tool schema.

- Set the whole look yourself from what the person expects: gender, age
  band, heritage, face shape, skin tone, skin texture, hair color, hair
  style, and the eye color, build, facial hair or makeup, and outfit that go
  with them. Keep every trait consistent with the others and with the
  heritage.
- Leave a trait out only when the person wants a surprise. Anything left out
  is picked at random, each on its own, without the brief or the other
  traits.
- Makeup and bust size are only for women, facial hair only for men. Set
  bust size only when the person asks.
- Who: match the gender, age band and heritage to the people the Brand sells
  to, unless the person says otherwise. When you make several options, make
  them clearly different people.
- Tone: skin texture, makeup and outfit set it. Natural skin, little makeup
  and everyday clothes read as a real person filming on their phone.
  Smoother skin, more makeup and a sharper outfit read as a polished ad.
  Match the content the avatar is for.
- When the look they want has no matching value, pick the closest one and
  put the rest in `notes`.
- `notes` is a light hint of mood or style, weaker than the traits. The
  scene, pose and setting come later, when the avatar is used.

## Make and save

- Make one avatar per draft: leave `count` out. For several options, make
  one each.
- Leave `names` out unless the person named the avatar. The server picks a
  name that fits the look.
- Pass `model`, and `quality` (`low`, `medium`, `high`) for a model with a
  quality setting, only when the person chose them, checked with
  `list_image_models`; otherwise leave both out.
- Save only an avatar the person picked or already asked you to save. For a
  new name, call `rename_avatar` first, then `approve_avatar`. Then say in one
  sentence that it is saved and ready for slideshows and videos.
- "Same person, but different X": copy that draft's traits, notes, model and
  quality, and change only X. Anything left out comes out different.
- If a draft has a problem, say what it is in one line and ask whether to try
  again. Do not remake it on your own.
- If making an avatar fails, say why in plain words. Do not retry or switch
  models unless the person asks. A new try after a failure is a new avatar
  with a new key.
- Pass one `idempotencyKey` per avatar. If a call timed out, was stopped, or
  its result is unknown, send the identical call with the same key: it
  returns the first avatar with no new charge. Never send a changed call with
  an old key. If you had no key, check `list_draft_avatars` first.
- Find a saved avatar's id with `list_avatars`; never guess ids.
- When the person already has photos of the avatar, have them upload each,
  then call `add_avatar_images` with the `mediaIds` and `avatarId`, or `name`
  for a new avatar. It is free and needs no approval.

## Cards

Call `list_workspaces` once. If it returns one workspace, use it without
asking; if several, ask which one. Pass that `workspace` on every write. If
two share a name, use the slug or id. To ask the person something, use the
host's own question UI if it has one; otherwise ask in one short message.

### In claude.ai and ChatGPT

- Every new avatar starts in the avatar builder, which replaces the
  questions. Call `render_avatar_builder` at once with the `workspace`, the
  whole look you chose as `traits`, the traits the person stated as
  `lockedKeys`, and the vibe in `notes`. Pass `randomize: true` only when
  they want a surprise. Then say in one short line that they can press
  Generate or change anything first.
- Never call `create_avatar` yourself. Generate shows the price, and its
  click is the person's approval. The builder makes the draft and shows it
  with a name field and Approve. It shares each draft with you without a chat
  message: its avatar id, name, whether it is saved, and its `Traits:`,
  `Notes:` and `Model:` lines. Do not wait for a message, render the draft
  again, or ask for names in chat.
- Approve on a card saves the avatar itself. Never call `rename_avatar` or
  `approve_avatar` after it.
- "Same person, but different X": copy the `Traits:`, `Notes:` and `Model:`
  lines the card shared into `traits`, `notes` and `model`, change only X,
  and open the builder again with every trait key in `lockedKeys`. If the
  host shared nothing, `list_draft_avatars` gives the draft's id and name;
  ask the person to press that draft's Edit or Recreate, whose message
  carries those lines.
- To show drafts you already have, call `render_image_results` with one
  ready `avatar-draft` item per image and its name as `title`. To show a
  saved avatar's photos, call `render_library`. Never hand-build a gallery.
- A Use click is not approval for paid work. Ask what they want to make if
  that is not known.

### In coding apps (Claude Code, Cursor, Codex)

These show no cards.

- Before `create_avatar`, say the model and the price in one sentence:
  `1 draft with {model label}, {price} credits`. Without a chosen model, use
  the `isDefault` model from `list_image_models`.
- After it is made, say in one or two lines what you made, put the draft's
  `dashboardUrl` on its own line, and end with
  `💳 {creditsSpent} credits spent, {creditsRemaining} remaining`. Then ask
  whether to save it, and under which name.
- A draft's traits are echoed in the result.
- Failed generations refund. The balance is shared with teammates;
  `list_transactions` with `mine: true` shows what this connection spent.
