---
name: 3d-cartoon-ads
description: The 3D cartoon look for video ads. The look of a family animated feature film. Use when the user asks for 3D animation, a 3D cartoon, an animated-movie look or a 3D mascot.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-ad-style-3d-cartoon` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

# 3D cartoon

A 3D cartoon ad looks like a scene from a family animated feature film. The
characters are rounded and appealing, with big expressive eyes, and the world is
lit with soft cinematic light. It is stylised, never photoreal.

What makes it work:
- Appeal: simple rounded shapes, clear silhouettes, big eyes with catchlights,
  proportions pushed past real life.
- Soft cinematic light: a warm key light, a rim light that lifts the character
  off the background, soft shadows.
- Rich but simplified materials: skin with a soft glow, fabrics and props a
  little simplified, never plastic or waxy.
- Acting that reads from across the room: big poses, clear faces, squash and
  stretch on impacts.

Say "stylised 3D animated" in every prompt; words like "realistic" or
"photoreal" pull the people towards uncanny. The product is the exception: it
stays accurate, with its real label.

Examples:
- "Stylised 3D animated feature-film scene: a round-faced boy with big brown eyes
  and messy hair gasps as his cereal bowl tips over at the breakfast table; warm
  morning key light from the window, soft rim light, shallow depth of field."
- "Stylised 3D animated scene: a cheerful round sun mascot hands the real
  sunscreen bottle, label accurate, to a girl on a bright beach; saturated
  colours, soft shadows, low hero angle."
- Video: "Animated-film motion: the bowl tips, cereal spills with a bounce, and
  the boy's eyebrows shoot up; slow push-in."

Any variation the user asks for (toy figure, bold mascot, painterly storybook) is fine; keep it stylised 3D.
