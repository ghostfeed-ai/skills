---
name: skeleton-animation-ads
description: The skeleton format for video ads. One recurring cartoon skeleton acts out a problem that gets worse step by step, then the fix. Use when the user asks for a skeleton ad, a "what happens if you…" ad, or a Day 1 to Day 365 progression.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-ad-style-skeleton` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

# Skeleton

A skeleton ad follows one cartoon skeleton through a story told to "you": "What
happens if you stop drinking water? Day 1… Day 7… Day 30." Each step is visibly
worse (or better) than the last, the product arrives on one clean turn, and the
story lands on a payoff.

What makes it work:
- A curiosity question as the hook: "What happens if you…", "What if you
  never…", "How long can you… before…".
- A ladder that climbs: by time (Day 1, Day 30, Day 365), by amount (1, 5, 25)
  or by stage. One line is one scene is one step.
- The same skeleton in every scene, from one locked picture: friendly cartoon
  eyes, real-looking bones, not scary, not toy-like (unless the brand is playful
  on purpose).
- Second person, present tense, one physical picture per line. Reaction
  characters around the skeleton make each step easy to read.

The skeleton can be bare, dressed for the theme (a suit, cowboy gear), or an
X-ray body with glowing organs for health products.

Examples:
- "Cinematic 3D render: a friendly ivory skeleton with large cartoon eyes slumps
  at an office desk at 3pm, its spine curved like a question mark; coworkers
  glance over; warm window light."
- "The same skeleton, standing tall at the same desk, sipping from the real
  electrolyte bottle, label facing camera; a coworker gives a thumbs up."
- Video: "The skeleton's knees buckle as it climbs the stairs, and it grabs the
  rail; slow push-in."

Any variation the user asks for (a different theme, era or world) is fine; keep
one skeleton and one climbing ladder.
