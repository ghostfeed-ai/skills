---
name: ghostfeed-slideshows
description: Drive Ghostfeed's TikTok photo-slideshow Director engine over MCP. Brief the server, poll the generation, review the deck, hand over the link. Refined from real founder dogfooding.
---

The server owns the composition. Its Director engine builds the deck in one
agentic loop: it writes the slide copy, searches Pinterest, looks at the
candidate images with its own vision, and casts each background from what it
saw plus any collections the brief mentions. It holds a hard quality bar (no
infographics, no baked-in text, no staged stock, no blurry images) and
re-searches on its own when a batch comes back weak. Before finishing it
inspects its own deck and repairs any gaps; if it still cannot finish, the
generation reports `failed` honestly instead of shipping a broken deck. You
contribute the brief going in and the review coming out; you never hand-place
images. Creation costs 1 credit, refunded automatically if the build ends
`failed`.

## The flow

1. Brief well. `create_slideshow` takes a required `workspace` and exactly ONE
   of `prompt` (create from
   an idea) or `sourceUrl` (remix a TikTok Photo Mode or Instagram post; the
   copy is rewritten in the same structure and every image re-cast). A strong
   prompt names the topic, the angle, the audience, and the voice ("warm
   big-sister voice for women on GLP-1 peptides"). Persona voices and brand
   vocabulary carry through faithfully, including substitute words: if the
   user's niche says "ratatouille" instead of the real term, state the
   substitution in the prompt and the whole deck will honor it. Omit
   `slideCount` unless the user fixed a number.
2. It is ASYNC. The call returns a `gen_` id immediately; the Director runs
   1 to 3 minutes. Poll `get_generation` until the state is terminal. Every
   poll carries `dashboardUrl`, so the user can watch it compose live even
   before it finishes.
3. Review before presenting. When the state is `succeeded`, call
   `get_slideshow` and READ the deck: slide texts, and each slide's
   `backgroundSource` (pinterest, collection, ai, image; older decks may say
   avatar). Summarize the arc
   in a sentence or two and note where the user's own images were cast. The
   composed visuals (text laid over image) exist only in the dashboard, so
   always hand over the link.
4. The dashboard auto-updates. Decks appear and flip from processing to ready
   in real time; there is nothing to refresh manually.

## Featuring the user's own images and products

- Mentioning is the ONLY way the user's own images enter a deck. Nothing
  from the library is used automatically; an unmentioned collection never
  contends. There is no project-level pinning.
- `list_collections` shows the workspace's image collections with real ids.
  Pass one as `collectionId` to MENTION it: its images then contend for the
  slides where they fit. Mention whenever the user says "use my images" or
  names a folder.
- `list_products` shows registered products with real ids and their
  `linkedCollections` (the product's own photo collections). Pass one as
  `productId` to weave that product into ONE slide in a soft
  peer-recommendation voice; its linked collections supply the plug slide's
  imagery automatically.
- A plug described only in the prompt ("mention my app at the end") works for
  the copy, but only `productId` (or an explicit `collectionId`) can put the
  product's own photos in contention. Prefer discovering the id.
- Sourcing wishes in plain prose are honored: "only use my photos" keeps
  Pinterest out, "don't use my collections" keeps mentioned collections out
  of casting.

## Workspaces

Call `list_workspaces` first and keep the chosen workspace slug or id. Reads
may omit `workspace` and use the credential's pinned read default. Every
workspace-scoped write requires `workspace`; never infer it from whichever
workspace the user last opened in the dashboard. List responses echo the
resolved workspace. A typo fails with remediation listing valid names, slugs,
and ids.

## Limits and errors

Free plan allows 1 slideshow project; the error's remediation says who can
fix it (upgrade or delete a project). A remix needs a valid TikTok Photo
Mode or Instagram post url; other urls fail validation with the accepted
forms spelled out.

## The money and link ritual

Creation is a paid action: `create_slideshow` costs 1 credit, and a build
that reports `failed` refunds it automatically, so the user never pays for a
deck they did not get. After a create call, state the spend on its own line:

```
💳 1 credit
```

Free operations (lists, reads, blank-deck edits, Pinterest search) get no
money line. If the user asks what is left, `get_credits` has the balance.

When a response carries `dashboardUrl`, end your reply with the door on its
own line:

```
🔗 {dashboardUrl}
```

One link even when several decks were made: the one the user cares about
most, or the list view.
