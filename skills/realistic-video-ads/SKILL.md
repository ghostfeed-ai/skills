---
name: realistic-video-ads
description: The realistic look for video ads. Real-looking people and places, like live-action footage. Use when the user asks for a realistic, live-action or photoreal ad with scenes we design.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-ad-style-realistic` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

# Realistic

A realistic ad looks like real footage: real people in real places, shot on a
phone or a film camera. Viewers forgive nothing here, so realism is won in the
start picture; the video only brings it to life.

The main person comes from the user's avatar, or a photo they attached, when
there is one. When there is none, make the start picture from the best
reference available and say once that choosing an avatar looks more real.
Extras, hands and people in the background are just described.

What makes it read as real:
- One light source you could point to: a window on the left, a lamp overhead,
  streetlights at night. Flawless studio light reads as generated.
- Lived-in places: a little clutter, worn surfaces, real objects.
- A named camera: a phone, or a 35mm cinema lens, with its depth of field and
  grain.
- Small imperfections: skin texture, a crease, a stray hair, a smudge on glass.
- Small, real actions in each clip; say exactly how the product is held.

Examples:
- "Realistic phone photo: the woman from image 1 sits on a worn sofa by a window
  on the left, holding the tea tin from image 2 in both hands, label facing
  camera; morning light, a folded blanket beside her, slight grain."
- "Realistic film still, 35mm lens: a man's hands unscrew the jar from image 2
  on a crumb-covered kitchen counter; pendant lamp overhead, shallow depth of
  field."
- Video: "Natural real-time motion: she lifts the tin, opens the lid and smiles;
  handheld, slight sway."

Any variation the user asks for (documentary, polished commercial, clean
product studio) is fine; keep it real.
