---
name: cinematic-product-ads
description: The cinematic format for video ads. A product film with no spoken words, built from macro details, a reveal and one moment of use. Use when the user asks for a cinematic product video, a product film, hero shots, a premium commercial with no voiceover or a mood film.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-ad-style-cinematic` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

# Cinematic

A cinematic ad is a product film with no spoken words. Macro details, a reveal
and one moment of use carry the feeling, and it ends on one line added in the
edit. The sound is instrumental music or the clips' own sound.

What makes it work:
- Beautiful, exact shots: the product keeps its real shape and label in every
  frame.
- Shot types that build: a macro texture (a pour, a drop, a fibre), a reveal
  from shadow, mist or fabric, what it is made of, one hand using it, and a
  final shot of the product at rest with clean space for the closing line.
- One slow camera move per shot (a push-in, an orbit, a rack focus), with
  physical motion inside the frame: liquid, light, steam, fabric.
- One light source you could name, and a light event when it helps ("a soft
  light sweep crosses the label").
- A person who returns in several shots gets one reference picture first,
  attached to every shot of them; described in words alone, they come back as
  a different face each time.

Open on the strongest picture; it is the hook. Something changes on screen every
second or two, even when shots hold longer.

Examples:
- "Macro shot: a single drop of golden serum slides down the side of the real
  amber bottle, label sharp; dark background, one soft light from the left."
- "The real perfume bottle rises out of dark rippling water, droplets running
  off the glass; low angle, a thin rim light."
- Video: "Slow orbit around the bottle as a light sweep crosses the label; no
  on-screen text, no dialogue."

Any variation the user asks for (calm and premium, bold and fast, warm and
homely) is fine; keep it wordless until the closing line.
