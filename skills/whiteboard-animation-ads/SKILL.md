---
name: whiteboard-animation-ads
description: The whiteboard look for video ads. An explanation drawn on a whiteboard while a voice explains, by a hand alone or by a presenter at the board. Use when the user asks for a whiteboard video, a hand-drawn explainer, a sketch explainer or a presenter at a board.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-ad-style-whiteboard` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

# Whiteboard

A whiteboard ad explains something by drawing it. A hand alone, or a presenter
standing at the board, adds one mark at a time while the voice says why. The
board is the story: it grows from empty to a full, readable picture.

What makes it work:
- Make the finished board first. Every earlier board is that picture with the
  newest marks erased, made one at a time from the board after it. Look at each
  before making the next: an erase that missed leaves marks the hand never
  draws.
- One clip per writing beat. Each clip starts on the board before its marks and
  ends on the board after them (its end frame), so the hand draws exactly those
  marks. Use a model that takes an end frame (`list_video_models`: `endFrame`).
- The same hand in every clip: describe it word for word the same (skin,
  sleeve, marker colour, the side it comes from).
- The board writing is the only text in the picture, spelled exactly. Short
  labels, large lettering.
- Real drawing speed: every clip says "natural real-time human speed, no
  timelapse or speed ramps".

Examples:
- "A clean whiteboard in a bright office, straight on. Already on the board: a
  stick figure on the left labelled 'YOU'. The rest of the board is blank."
- Video: "Natural real-time human speed, no timelapse or speed ramps: a right
  hand with a grey sleeve and a black marker comes in from the right, draws a
  downward arrow from 'YOU' to the empty right side and writes 'TIRED' under
  it; all existing marks stay unchanged."

Any variation the user asks for (a chalkboard, a notepad, coloured markers) is
fine; keep it drawn live.
