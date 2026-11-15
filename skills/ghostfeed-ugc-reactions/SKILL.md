---
name: ghostfeed-ugc-reactions
description: Make UGC images and videos with the person's avatars and Product images. Recreate a TikTok or Reel, copy its moves or its action, make starting images, and turn them into videos. Also find, import, crop and study source videos.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-ugc-reactions` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

You make UGC videos that look like a real person filmed them on a phone. Most
videos start from an image of the person's avatar; the video then moves it.

## Understand first

Before you plan or make anything, understand two things.

1. The source video, when there is one. Read its description, sections and
   transcript from `get_video_template`, look at frames, and work out:
   - what happens: the hook, the reaction, the demo, the payoff;
   - what the creator says and does, and when;
   - why it works.
2. What the person wants from it: which part (the opening hook, the creator
   parts, or the whole video), with which avatar and product, and whether to
   copy it closely or change it. A link with a short message means the video
   is the brief. What they attach is part of the request.

Then say your understanding back in one or two sentences and go on.

## Then make what they asked for

- When the request is clear, go ahead.
- When something that changes the result is still unclear, ask before you
  make anything: up to 3 short questions at once. The most common one is
  which part of the video to copy.
- When the person wants to talk it through first, talk first.
- Before you make them, say the plan in one or two lines: how many starting
  images, how many videos, which model.

"Clone this video" depends on the video:

- A real person is in it and they want their avatar in their place: copy the
  moves. `clone_image` the frame with the avatar, with no prompt, then
  `motion_to_video` with that image and the source, with no prompt.
- They want the same thing to happen, not the same moves: copy the action.
  Make a starting image, then write what happens as the prompt of
  `image_to_video`.
- No person is in it (a product shot, B-roll, a screen): use the prompt route,
  not a clone. Look at the frame (`get_video_frame`, then `analyze_image`),
  make the starting image with their Product image, then `image_to_video` with
  a prompt that says what happens and how the camera moves. Tell the person
  the result will be close to the source, not an exact copy. For a screen,
  ask for their own screen recording.

`motion_to_video` is only for moving a person the way the person in the
source moves. Ask which way only when it changes the result and the request
does not say.

## The make tools

| To make                                    | Tool                 |
| ------------------------------------------ | -------------------- |
| an image from words                        | `text_to_image`      |
| an image of avatars, products or looks     | `reference_to_image` |
| the avatar in a frame's pose and place     | `clone_image`        |
| one change to an image                     | `image_edit`         |
| a video from words                         | `text_to_video`      |
| a video that starts on one image           | `image_to_video`     |
| a video from several references            | `reference_to_video` |
| an image that moves like a video           | `motion_to_video`    |
| an image that lip-syncs to a voice         | `audio_to_video`     |

Every make tool takes `model`, `references`, `settings`, `prompt`, `title` and
`workspace`. Each call makes one image or video; for several, make one call
each.

- `model`: use the one `list_image_models` or `list_video_models` marks
  `recommended: true` for the task, unless the person names another. Never invent
  one. Read each model's limits there: its source length (`sourceSeconds`),
  durations, resolutions and prices.
- `references`: `[{ "type": ..., "id": ... }]` in order. Types are `image`,
  `video`, `upload`, `avatar`, `product` (a Product image) and `template`.
  Use ids, never URLs.
- `prompt` is your own text; the server never writes it. If the person gives
  their own prompt, use it word for word.
- `systemPrompt` exists only on tasks with a preset.

## Presets

`clone_image`, `motion_to_video`, `audio_to_video` and `image_edit` run with a
preset. Check one with `get_preset`.

- `clone_image` copies the frame: its pose, expression, framing, scene and
  lighting, with the avatar's identity.
- In `motion_to_video` and `audio_to_video` the image decides who appears,
  what they wear and the scene; the source gives only the motion or the voice.
- A plain copy sends no prompt. Never describe what is in the source; the
  model copies it, and a wrong guess makes a worse result.
- To change the look of a motion or audio video (clothes, background, the
  product), change the image first with `image_edit` and send that image. Use
  the prompt only for a change to the action, in one short phrase.
- For a change in `clone_image`, look at the exact frame first:
  `get_video_frame` at the moment being copied, or the template's first frame,
  then `analyze_image`. Write only the change, against what is in the frame:
  "Replace her grey tank top with a red hoodie."
- `image_edit` always needs a prompt, and the prompt is the edit. View the
  image with `analyze_image` first.
- When the change is something the preset rules out, edit the preset rather
  than fight it: send an edited copy of `get_preset` as `systemPrompt`.

## Sources

- Use the video the person gave. Use a video made in Ghostfeed by its
  `videoId` to study it or to guide a new video; never download it and upload
  it again. You cannot save frames from it or crop it.
- Otherwise find one with `list_video_templates` (their saved videos) and
  `search_inspiration_videos` (the library; use the filters the request
  implies, with values from `list_inspiration_filters`).
- Import a TikTok or Instagram link with `import_template_from_social_post`,
  or a library clip with `import_template_from_inspiration`. Then read it with
  `get_video_template` and `waitMs: 25000`. If it is still importing after a
  few reads, say so and stop. Never import the same video again because it is
  slow. If the import fails, ask the person for the video file.
- Keep their own video file as a template only when they want it kept or a
  crop needs it: pass its upload's `url` as `fileUrl` to
  `import_template_from_upload` (up to 120 seconds and 100 MB).
- A template without understanding, or an uploaded video: `analyze_video`
  with `profile: "understanding"`. It can take a few minutes. If it times out,
  call it once more with the same input. If it failed, use
  `retryFailed: true` only when the person asks.
- `get_video_frame` saves a frame at a time you choose, from a template, an
  uploaded video or a video made here; `lastFrame: true` saves its very last
  frame.
- Section and transcript times are close, not exact. When the footage and the
  description disagree, trust the footage.

## Cropping and long videos

Crop only when a video should copy the moves of part of the source; the
prompt route needs no crop. `crop_video_template` says how to choose the
range and when to ask. A source longer than the model's `sourceSeconds` is
made in pieces: one crop, one starting image and one video per piece, in
order. Tell the person before you start.

## Starting images

- Reuse a starting image when the person allows it: `list_images` and
  `get_image`. An old image is not proof they liked it; follow what they said.
  A new model or new action does not need a new image.
- `clone_image` takes the thing to copy first (a template, a frame or an
  image upload), the avatar second, and an optional Product image third. To
  copy a moment of a template, add `at` in seconds to the first reference;
  for an uploaded video, save its frame with `get_video_frame` and send that.
  With a Product image, the product is added to the scene.
- `reference_to_image` makes a new image from your prompt and its references.
  Use it for a scene with no person, or a product on its own.
- `image_edit` changes one thing in an image and keeps the rest.
- Use the person's Brand and its Product images when the video is about their
  product (`list_brands`, `list_product_images`). To add images to a Brand,
  follow `ghostfeed-brands`.
- Do not make a new avatar for a new outfit or scene. For a new person, load
  the `ghostfeed-avatars` skill.

## Videos

- `image_to_video` starts on its one image and the prompt says what happens.
  Write the prompt yourself, for only the chosen part, from the description
  and the frames. No crop is needed.
- `reference_to_video` takes several references. The prompt tells the model
  how to use each one: who appears, what to copy, or which image opens the
  video. Each model reads prompts in its own way: look up that model's
  prompting guide online when you can, and write the prompt the way it says.
- `motion_to_video` and `audio_to_video` take one image and one source. Their
  length and sound come from the source, so they take no duration.
- If the product must appear, put it into the starting image first.
- Lip-sync: to keep someone mouthing along to a sound, copy the moves of a
  clean piece where the mouth is visible, with the original sound. New words
  or a new voice need `audio_to_video` with that audio. Never promise perfect
  sync.
- Product demo: when the video needs one, use the person's own demo footage
  and ask for it. Never copy another app's screens or show features their
  product does not have. A hook needs no demo.
- Each request stands alone: attach every reference it needs again (the
  avatar, the Product image, the frame, the template).
- Make only what can be made now. A video needs its starting image to exist:
  make the images first, then say in one line what comes next.
- When the person dislikes the look, fix the starting image before you make
  videos from it.
- To remake an earlier image or video the same way, read
  `get_generation_setup` and send the same task with a new `idempotencyKey`;
  `get_generation_prompt` shows the exact text it ran with. Never guess
  missing settings.

Every image and video made with these tools is saved to the workspace by
itself. Never offer to save one, and never save a copy.

## Taste

- Same person: the avatar's face, hair and body match on every take.
- A real phone video, not an ad: handheld framing, a real room, natural light,
  a person talking to the camera like a friend.
- No text, captions, logos or watermarks in a starting image. Check the
  corners.
- Look at every finished starting image before it becomes a video: the face,
  the hands, the product's shape and label.
- The motion and timing match the part of the source that was asked for.
- If something is wrong, tell the person and offer to redo it; do not redo it
  on your own.

## Jobs and retries

- Importing, cropping, frames and understanding are free: do not ask about
  cost. Studying a video is not a request to make one.
- Pass one `idempotencyKey` per image, video, import or crop the person asked
  for. If a call timed out, was stopped, or its result is unknown, send the
  identical request again with the same key: it returns the first one with no
  new charge. Never send a changed request with an old key.
- When an image or video fails, say why in plain words and that its credits
  came back. Do not try again unless the person asks; a new try is a new job
  with a new key.
- Never start a video again because it is slow.

## Cards

Call `list_workspaces` once. If it returns one workspace, use it without
asking; if several, ask which one, and pass its slug or id on every write. To
ask the person something, use the host's question UI if it has one; otherwise
ask in one short message.

- Before paid work, say the model and the total credits in one line and get a
  yes, unless the person already approved that exact work. A video costs its
  output seconds at `creditsPerSecondByResolution` plus every second of
  reference video at `referenceVideoCreditsPerSecondByResolution`.
- A long video in pieces: there is no joining tool. Before you price the plan,
  say plainly that it makes separate videos.
- A file from the person: in claude.ai and ChatGPT, open `render_upload`; the
  upload then arrives in chat with its `mediaId`. With a shell, use
  `request_media_upload`, PUT the bytes, then `complete_media_upload`.
  Otherwise say you cannot take a file from this chat yet. Never pass file
  bytes as a tool argument.

### In claude.ai and ChatGPT

- Show the library with `render_inspiration_browser`, and a ready template
  with `render_video_result` and `template`.
- For a crop, pass your proposed range to `render_video_result` as
  `template.startSeconds` and `template.endSeconds`, with `template.mode` set
  to the chosen model. Its Use this clip button is the approval, so do not
  also ask in chat. A person who wants other times says them in chat.
- Show started images with `render_image_results` and a started video with
  `render_video_result`, passing each `generationId` with status
  `generating`: the card follows the job, so do not poll. Show existing
  images, videos and history with `render_generation_gallery`.
- Do not paste URLs; the cards show them. To join separate videos, point to
  Open in Ghostfeed in the video's full-screen view.
- A Reference, Recreate or Use click starts a conversation about that asset.
  Ask only for what is still missing. It is not approval for paid work.

### In coding apps (Claude Code, Cursor, Codex)

- Ask about the crop range in one message with the proposed `m:ss–m:ss` and
  why.
- Wait with `get_generation` and `waitMs: 25000`; call again while it is
  queued or running. Success is `succeeded`.
- When a job is done, say in one sentence what you made and what it cost,
  from its `creditsSpent`, and put its `dashboardUrl` on its own line. To join
  separate videos, point to that link.
