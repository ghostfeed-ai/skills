---
name: ghostfeed-ad-style-2d-cartoon
description: The 2D cartoon look for video ads. Hand-drawn animation with clean lines and flat or cel-shaded colour. Use when the user asks for 2D animation, a cartoon, hand-drawn, flat illustration, anime-style or doodle.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-ad-style-2d-cartoon` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

# 2D cartoon

A 2D cartoon ad looks like hand-drawn animation: clean line art, flat or
cel-shaded colour, and painted backgrounds that sit behind the characters like a
separate layer. There is no 3D volume and no rendered gradients.

What makes it work:
- Clear outlines with a steady weight, and a small named palette.
- Flat colour, or cel shading with one crisp shadow tone.
- Simple scenes: one subject, a clear silhouette, a background that does not
  compete. Busy detail flickers once it moves.
- Drawn motion: held poses, snappy changes, smears on fast moves; no orbits,
  since a 2D character has no back.

Say "2D hand-drawn animation, no 3D render" in every prompt, or it drifts to 3D.
The product is drawn in the same style, keeping its real shape, colours and label.

Sub-looks the user can pick:
- Flat vector: geometric characters, dot eyes, flat fills, bright palette.
- Classic cel: inked outlines, cel shading, lush watercolour backgrounds.
- Anime-inspired: fine lines, large bright eyes, detailed painted skies.
- Doodle: loose pencil and marker lines, colour that doesn't quite fill them,
  off-white paper.

Examples:
- "2D hand-drawn animation, no 3D render, classic cel: a fox in a yellow scarf
  slumps at a café table, a scribble cloud over his head; watercolour street
  behind; warm orange and teal palette."
- "2D flat vector animation, no 3D render: a smiling woman holds up the real
  water bottle, label kept, against a flat mint background."
- Video: "2D hand-drawn motion on twos, line art stays stable: the fox perks up
  and his ears pop up with a smear; static camera."

Any other 2D variation the user asks for is fine; keep it hand-drawn and flat.
