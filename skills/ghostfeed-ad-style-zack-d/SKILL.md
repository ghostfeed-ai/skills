---
name: ghostfeed-ad-style-zack-d
description: The Zack D style for video ads. A 3D explainer where the camera travels inside the problem and the product in one continuous journey while a calm voice explains. Use when the user asks for a Zack D or Zack D Films style, a "what happens inside" explainer, a how-it-works video or a 3D science ad.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-ad-style-zack-d` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

# Zack D style

A Zack D style ad is a 3D explainer that shows what happens inside: inside the
body, the skin, a machine, the product. A calm, curious voice explains one
surprising thing in short plain sentences, while the camera travels through
the problem and the product in one continuous journey. Each change of place is
a designed move (into a pore, out of a capsule), not a cut every few seconds.

What makes it work:
- A clean, softly lit colour world the ad keeps returning to. Describe it as a
  world the camera stands inside that goes on past the edges of the frame.
  Never write "stage": it draws a literal theatre stage with an edge.
- Objects rest on the ground with a soft contact shadow. Never write "floating"
  or "hovering"; objects look pasted in.
- Numbers and claims are solid 3D objects with light and shadow (gold numerals,
  a red X), not flat text.
- Colour carries meaning: the world washes red for danger, green for the fix,
  gold for the win, then returns to its base colour.

Make the world first: one empty picture of it, attached to every start
picture, so every scene sits in the same world. Plan the journey: each clip
ends where the next picture begins (the camera pushes into the pore; the next
picture is inside the pore), and every clip prompt ends with that move. Send
the next picture as the clip's end frame, so the move lands exactly there.
One big subject fills each picture, close or from a low angle, never small
figures in empty space. A body seen from the outside wears clothes; a bare or
see-through body comes out looking nude.

Examples:
- "Stylised 3D render: a giant skin pore seen from inside, cracked dry walls,
  dry skin flakes resting on the surface with soft contact shadows; a
  soft blue world beyond, no edges."
- "Stylised 3D render: raised gold numerals '8 HOURS' standing on a soft cyan
  ground that continues past every edge of the frame, one warm key light."
- Video: "One continuous move: the camera pushes into the pore and comes out
  inside the moisturiser jar."

Any rendering the user asks for (claymation, paper) is fine; keep the calm
voice and the continuous journey.
