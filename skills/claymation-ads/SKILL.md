---
name: claymation-ads
description: The claymation look for video ads. Everything on screen is made of clay. Use when the user asks for claymation, clay, plasticine or a stop-motion look.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-ad-style-claymation` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

# Claymation

A claymation ad looks like a stop-motion film shot on a miniature clay set.
Everything in the frame is sculpted plasticine: the people, the product, the props,
the floor, the sky. Nothing is a photo or a smooth 3D render.

What makes it read as clay:
- Hand-made surfaces: fingerprints, tool marks, a soft matte sheen. Words like
  "smooth", "glossy" or "polished" turn it into CGI.
- A miniature set in bright, warm light, the camera inside the clay world. Dusk
  and dark scenes lose the clay look, and cold light (a fridge, a phone screen)
  turns clay skin blue, so state the skin's own colour ("her terracotta clay
  skin").
- Clay hands: "sculpted clay hands, blunt tips, no fingernails", or they come out
  as real human hands.
- Stop-motion movement. Every clip says: "12fps stop-motion cadence, no motion
  blur, not CGI."

The product is sculpted in clay with a real printed paper label, its words written
out, or the word "clay" leaks onto it ("CLAY CAFÉ"). Glass, liquid and metal are
"a clay imitation of …".

Examples:
- "Claymation scene: a plasticine woman with thumb-smoothed cheeks yawns in a clay
  kitchen at sunrise, holding a clay coffee mug; sculpted clay hands, blunt tips,
  no fingernails; fingerprints on every surface; warm light on a miniature set,
  camera at eye level inside the scene."
- "Claymation scene: a clay honey jar with a real printed paper label reading
  'WILD MEADOW HONEY' sits on a sculpted wooden table as a clay bee lands on
  the lid; macro lens, soft background blur."
- Video: "12fps stop-motion cadence, no motion blur, not CGI: the bee lands and
  the jar wobbles once."

Any variation the user asks for (goofy, puppet-like, minimal) is fine; keep it all clay.
