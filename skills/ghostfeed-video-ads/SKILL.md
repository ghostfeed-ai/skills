---
name: ghostfeed-video-ads
description: Make a product video ad, from a script, a song or a scene idea to one finished video. Use when the user asks for a video ad, a commercial, a product video, a music-video ad, a talking mascot, a Zack D style explainer, a whiteboard video, a skeleton ad, a cinematic product film, or an ad in a look such as claymation, paper, 3D or 2D cartoon or realistic. Realistic UGC creator videos, reaction videos, recreating a video the user shares and animating one image belong to ghostfeed-ugc-reactions.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-video-ads` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

A video ad: know what you're promoting, pick the look, decide how it sounds,
plan the scenes, make the pictures and clips, put them together.

## What the user gave is settled

Use their script, lyrics, song, recording, pictures, avatar, product, look,
story, model or length as given: don't rewrite it, research it again or ask
about it again. A story they tell is the plan: its people and its turns are on
screen. If something they gave can't work as given, say what and ask. Ask only
what they didn't say and what changes the ad, a few short questions at once in
plain text, your recommendation first. Small things are yours to decide. Skip
any step that doesn't apply: "make my avatar say hello" is one clip.

## Looks and other skills

Load each with `get_skill` by its exact name when it's needed. Use every look
the request names or implies; when the user names no look, ask.

| Look                                                        | Skill                           |
| ----------------------------------------------------------- | ------------------------------- |
| Everything is clay                                          | `ghostfeed-ad-style-claymation` |
| Everything is paper                                         | `ghostfeed-ad-style-paper`      |
| An animated feature film                                    | `ghostfeed-ad-style-3d-cartoon` |
| Hand-drawn animation                                        | `ghostfeed-ad-style-2d-cartoon` |
| Real-looking people and places                              | `ghostfeed-ad-style-realistic`  |
| An explanation drawn live on a whiteboard                   | `ghostfeed-ad-style-whiteboard` |
| Zack D style: the camera travels inside the body or a thing | `ghostfeed-ad-style-zack-d`     |
| A skeleton acts out a problem and its fix                   | `ghostfeed-ad-style-skeleton`   |
| A product film with no spoken words                         | `ghostfeed-ad-style-cinematic`  |

Also: `ghostfeed-song` for a song, `ghostfeed-ad-copy` for the words,
`ghostfeed-ad-characters` for characters and reference pictures,
`ghostfeed-avatars` for a new realistic person, `ghostfeed-brands` when the
product has no Brand.

## On MCP

- Call `get_me` and `list_workspaces` first, and pass the workspace on every
  write.
- Every paid call spends credits at once; there are no drafts. Before each
  paid step (a song, a voiceover, a sheet, the start pictures, the clips, a
  remake), say what you'll make and its credits, and wait for the user's go.
  Check the total with `get_credits`.
- Making is asynchronous. In an MCP Apps host, show each generation with
  `render_image_results` (up to 4 images) or `render_video_result`; otherwise
  wait with `get_generation` and `waitMs: 25000`, and share each result's
  title and link. A song or voiceover has no view, so always wait for it.
- Joining clips and cutting audio need the host's shell with ffmpeg; check
  once with `ffmpeg -version`.

## Steps

1. **What it's for.** The Brand and Product image being promoted, the look,
   the length. The shape is 9:16 unless the user says otherwise.
2. **Words.** The user's script or lyrics as given; otherwise write them with
   `ghostfeed-ad-copy`. About 2.5 words a second, spoken or sung. Show them
   before making anything that depends on them.
3. **Reference pictures.** What keeps characters, places and the product the
   same: a character sheet for a drawn or sculpted look, the user's avatar or
   a sheet for real people, an empty picture of a place the ad stays in (a
   kitchen, a Zack D world), the Product image. An avatar is a face, not a
   scene. Attach each to every picture that shows it.
4. **Sound.** One of these, or a mix:
   - **Characters speak.** The video model voices their lines in the clips;
     nothing else is made. Every clip makes a new voice, so put each
     speaker's lines in as few clips as fit. Lip-sync only when the user asks
     for it.
   - **Narration.** A voiceover over the ad: `text_to_speech`, or the user's
     recording. The characters don't speak. Let the user pick the voice by
     listening to a few from `list_voices` (each has a preview link).
   - **Song.** A song over the ad: load `ghostfeed-song`, or use the user's
     song.
   - **No words.** The clips' own sound, or instrumental music.

   Make the voiceover or song first and wait for it: its word timings
   (`get_audio_timings`) set each scene's length, so no clip is made before
   it. A whole song or take attaches to a clip by its id
   (`{ type: "audio", id }`), like a picture; a part of one is cut with ffmpeg
   and uploaded (`request_media_upload`, PUT the file, then
   `complete_media_upload`).
5. **Start pictures.** First show the plan as a table, one row per clip: the
   time and the line said or sung, or what it shows, 160 characters at most,
   with the credits for the pictures and the clips. Then, before any clip,
   make each clip's first frame as a 9:16 picture in the ad's look, with its
   reference pictures attached. Each turn of the story gets its own picture
   with the people in it (the ones who stay lean, the one who hands over the
   secret), not only the narrator. Every clip starts from its picture
   (`image_to_video`); a clip made from text or from reference pictures alone
   invents its own room, so the scenes stop matching. When the next scene
   continues this clip with no cut (one camera move, a board that keeps
   growing), send the next clip's start picture as this clip's end frame, on a
   model whose `list_video_models` entry says `endFrame`. A start picture is
   one moment from one camera: two shots in one prompt ("…, then …") come back
   as a collage. Look at every start picture before writing its clip (in the
   chat when the host shows images, otherwise with `analyze_image`), and
   remake one that broke (a collage, the wrong room, a pasted photo, a changed
   face). The user sees them and changes what they want.
6. **Videos.** Write good prompts from what the user asked (below). One clip
   can hold several shots; name each cut. Make the clips.
7. **Put it together**, by sound:
   - Characters speak: check the clips, join them, keep their sound.
   - Narration or song: join the clips, mute their sound, lay the voiceover or
     song on top.
   - One clip: it is the result.

   Never cut the voiceover or song: it plays as one take, start to end, and
   the picture is fitted to it. Each clip fills the time from its line's
   first word to the next line's first word (the first from the start, the
   last until a second after the last word). Speed clips joined by end frames
   up or down to fit, since cutting either end makes the picture jump at the
   join; trim the others at the end. Bring the finished sound to about
   -14 LUFS.

   With a shell, download the clips and the audio with curl, join them with
   ffmpeg and give the user the file's path. Without one, say the video isn't
   joined yet, and give the clips in order with their links and the audio to
   lay under them. Add captions only when the user asks. Check the result once
   (the start, a cut, the end) before you say it's done.

## Prompts

- Say what each attached picture is for ("image 1 is Maya, image 2 is the
  product"), and never describe what a picture already shows.
- One action and one camera move per shot; name every cut or transition.
- Change the camera angle and framing from scene to scene (low angle,
  close-up, over the shoulder, top-down); a person standing centred and
  facing the camera in every scene looks like a catalogue.
- A Product image shows the product's shape and label. In a clay, paper or
  2D look, describe its shape, colours and label words and say to make it in
  that look; asking to keep it "exactly as in the image" pastes the photo in.
  Attach it only to scenes that show the product, and keep it out of the
  hook. When the story names another container (a bottle, a jar), recommend
  the real product from the Product image.
- Spoken lines: the speaker, a verb, the line in quotes, then one delivery
  note. For dialogue, write "Line 1", "Line 2" with a Delivery note under each,
  keep the camera still and leave natural pauses.
- Describe each speaking character's voice (age, tone, accent, pace) and paste
  the same description, word for word, into every clip they speak in.
- No invented text, logos or captions in any picture or clip; the product
  keeps its real label.
- Never put labels or headings in a picture prompt ("TOP LEFT:", "Scene 1:");
  the model writes them into the picture. Say where things are in plain words.
- Effects that don't render well (scent, steam, molecules) are shown as a
  reaction or an object: someone sniffing their wrist and grimacing.
- The model, length, resolution and shape go in the call's fields, never in
  the prompt.

## Facts

- Video models: P-Video for an animated look with no real people when
  `list_video_models` has it, Wan 3 for real people, otherwise the one marked
  recommended. Read each model's limits there.
- Every new item and every remake gets a new `idempotencyKey`. A call that
  timed out is sent again unchanged, with the same key.
- To start a clip exactly where a finished one ended, take its last frame
  with `get_video_frame` (`source: { videoId }`, `lastFrame: true`) and use it
  as the start picture.
- A song is 1 credit for two versions; a voiceover 1 credit per started 1,000
  characters. Report what each result actually spent (`creditsSpent`).
- Copying a video the user shares belongs to `ghostfeed-ugc-reactions`.

## Fixes

Find exactly which part the user means, change only that, and say in one line
what you changed. When a clip misses, fix what caused it (the reference
picture, the start picture or the prompt) instead of making the same thing
again. When something fails, say plainly what happened and whether its credits
came back.
