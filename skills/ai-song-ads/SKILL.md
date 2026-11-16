---
name: ai-song-ads
description: Write and make an original song for a video ad with text_to_music, and use it as the ad's soundtrack. Use when an ad is carried by a song, a jingle or a music video, or when the user wants a song for their product.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-song` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

# Song

A song ad plays like a short music video: an original song carries the product
story, and every scene shows what the lyric says. It works when the song is a
real song people would listen to, not a jingle, and its hook lands the
product's point in the first 3 seconds.

## The lyric

- One sung line is one shot: 6 to 9 words a line, each about 2–3.5 seconds.
- Size it by sung words (section tags like [Verse] don't count): about 40 words
  for 15 s (a hook and one chorus), 75 for 30 s (verse, chorus, verse,
  chorus), 150 for 60 s (a full song with a bridge). About sung words ÷ 2.5
  seconds.
- The user's lyrics are used exactly as given.

## The style

The prompt is the style, under 25 words: genre, vocal (e.g. "female lead"),
tempo or BPM, mood, production. Never an artist or band name; the provider
refuses it. Suno sings the whole lyric only when told, so a style with vocals
ends with "vocals from the first second, no intro, tight ending".

Example: "Upbeat indie pop, warm female lead, 118 BPM, playful, polished,
vocals from the first second, no intro, tight ending."

## Making it

`text_to_music` with the lyrics in `settings.lyrics`, the style as `prompt`
and a `title`. Leave `settings.duration` out: the length is set from the lyric.
One call returns two versions. Share both links and let the user listen and
choose. You can't hear them, so never mark one as recommended.

## Using it

- `get_audio_timings` gives the finished song's word timings: each sung line's
  time is its shot's time. Make one clip for every one or two sung lines
  (about 8 clips for a 45-second song), so the picture changes when the words
  do.
- Nobody sings on camera unless the user asks for it; the clips are silent
  picture under the song. When they ask, the song attaches to that clip by its
  id, like a picture, and the clip is lip-synced to its part of the song.
- Cut the song with no gaps; only the silence before the first word may be
  trimmed. Never make one section of a song again: a new take won't match the
  rest.
- To finish, join the clips, mute their sound and lay the whole song on top.
