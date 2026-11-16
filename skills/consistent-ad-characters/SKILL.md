---
name: consistent-ad-characters
description: Designing a recurring character for a video ad and locking characters, the product and places as one reference picture each. Use before making reference pictures, or when the user wants a character sheet, a mascot, a product sheet or the same character across scenes.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-ad-characters` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

# Characters and reference pictures

Anything that appears in more than one scene gets one locked reference picture,
attached to every scene it appears in: a character, the product, a place.
Never use an earlier scene as the source for the next; small changes add up.

The reference picture for each:
- A stylised character: a character sheet in the ad's look.
- A realistic person: the user's avatar, or a sheet when there is none.
- The product: its Product image. Make a product sheet only when the images miss
  a side, a state (open, in use) or how it is held.
- A place: a sheet only when the same space returns in several scenes.

A good character is chosen on purpose, not left at defaults: one memorable
silhouette, a shape that fits the role (round is friendly, sharp is sly), one
signature detail, and the Brand's colours. Write it as one line that names every
choice, so the user can correct it: "Juno, a tallow jar with big round eyes on
the label, stubby arms, cream and gold, a tiny leaf on the lid."

A character sheet shows the same character from the front, side and back at the
same scale, plus close-ups of the face and the signature detail, on a plain white
background with no text.

Hard facts:
- A product with several parts: name every part and how it attaches, or it comes
  back as one sealed object. "Three parts: a lid, a cup open at both ends, a
  motor base; the cup screws onto the base."
- Write emotion as the face: "inner brows pushed up, mouth pulled flat", not
  "disappointed", which gives a neutral face.
- To put an avatar into a scene picture, route each part explicitly and add
  nothing else: "Take the face and hair from image 1. Take the pose, scene and
  exact object counts from image 2. Do NOT take face, skin or hair from
  image 2."

Examples:
- "Character reference sheet in the claymation look: Juno, a tallow jar with
  big round eyes on the label, stubby arms, cream and gold, a tiny leaf on the
  lid; front, side and back views at the same scale, close-ups of her face and
  the leaf; plain white background, no text."
- "Product sheet: the exact blender in the attached image, three parts (a lid, a
  cup open at both ends, a motor base; the cup screws onto the base); closed,
  taken apart, and in a hand; plain white background, no text except its real
  label."
