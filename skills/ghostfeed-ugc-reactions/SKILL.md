---
name: ghostfeed-ugc-reactions
description: Create UGC reaction videos over MCP the way the dashboard does. Get a template, render an avatar into the source pose (the first frame), get the user to approve that frame, then animate it. Two families, clone the reference motion or a prompt. Refined from real founder dogfooding.
---

The tools enforce the hard rules server-side: every write is workspace-scoped,
credits are charged and reported for you, the duration limits are applied on
import, and the flow is fixed at two phases (frame, then video). This skill makes
you read the user's intent and run the flow well on top, and it makes the frame a
real checkpoint.

This is a thin remote control for the dashboard flow, not a new engine. You do
not reinvent anything. You quicken the click path over chat: pick a template,
render the frame, get a yes, animate it.

## Library-first casting

For every reaction request, prefer Ghostfeed's reusable clip libraries before
making a custom first frame. Follow this order unless the user explicitly names
or supplies an exact source:

1. Search `list_reaction_templates` for a suitable opening pose in the
   workspace's owned and stock templates. Judge candidates by `opensOn`, then
   use `motion` only to decide whether the source performance is also useful.
2. If no template is suitable, search `list_inspiration_reactions` the same way.
3. Only after both libraries have no reasonable opening-pose match, fall back to
   `referenceImageUrl` from an avatar photo, user reference, or external image.
   Tell the user briefly what the library lacked and why a custom frame is
   necessary.

A custom motion request does not imply a custom first frame. A template or
inspiration can supply only the opening composition while a prompt mode animates
the approved frame from the user's words. Do not paste the library clip's
`motion` into the video prompt unless the user asked to reproduce that motion.
Do not search the web or browse avatar photos for a source until the two
Ghostfeed libraries have been checked.

## The flow

1. Orient a new user before choosing a source. Explain the two phases in plain
   language: first Ghostfeed makes a cheap still frame for approval; only then
   does it spend on motion. Also explain the two motion choices: **1:1 clone**
   follows the source video's performance and takes no motion prompt;
   **prompt-directed** uses the source only for the opening composition and
   follows words the user approves. Ask which outcome they want instead of
   assuming they know the distinction.

2. Get a source, following the library-first order above. A template is a source
   motion clip. Four ways in:
   - Use one that exists: `list_reaction_templates` (stock plus the workspace's
     own). You cannot watch the motion, so if the user must choose, describe the
     options from name and category, do not pretend to have seen them.
   - Import from a link: `import_reaction_template` with `sourceUrl` (a TikTok or
     Instagram link).
   - Import a local file: `request_reaction_upload` returns a short-lived
     `uploadUrl`. PUT the raw file bytes to it with the given Content-Type (for
     example `curl -T clip.mp4 -H "Content-Type: video/mp4" "<uploadUrl>"`), then
     `import_reaction_template` with `uploadedFileUrl` set to the returned
     `fileUrl`.
   - Reuse an inspiration clip: `list_inspiration_reactions`, then pass its id to
     `generate_reaction_frames` or `import_reaction_template`. It is auto-saved to
     the workspace as a template first and the new template id is surfaced.
     Import is async and free. Poll `get_generation` until terminal. `succeeded`
     means ready. `needs_action` means the source is 30 to 120 seconds and must be
     cropped in the dashboard first, so open the `dashboardUrl` and hand that step
     to the user. Over 120 seconds is rejected.

3. Render the first frame. `generate_reaction_frames` with the source (a
   `templateId`, an `inspirationId`, or a `referenceImageUrl`) and one or more
   `avatars` (names or ids, up to 10). It makes ONE frame per avatar. Poll each
   returned generation until `succeeded`. The frame image is `output.url` and
   `output.id` is the `frameId` you carry into the video phase. It uses
   `gemini_flash` unless the user asks for another model (`list_image_models`).
   Before calling it, state: “First frame: Gemini Flash, standard resolution”
   (substitute the actual selected values) and tell the user they can ask for a
   different listed image model or 1080p. Keep this to one sentence unless they
   ask for options.

4. Get the frame approved. This is the milestone, treat it as a hard stop. Show
   the user the rendered frame or frames and get an explicit yes that the avatar
   looks right BEFORE any video. The frame costs a fraction of a video, so this is
   where you catch a bad render cheaply. If a frame is off, `regenerate_reaction_frame`
   with that generation's id for a fresh take. Never start a video on a frame the
   user has not approved. For every succeeded frame, download `output.url` to a
   temporary local file and attach it in the approval reply, following
   Delivering assets in chat below.

5. Prepare and approve the motion settings. Call `list_reaction_video_modes`
   before the first video in a conversation. State the selected mode/model,
   duration behavior, output resolution, audio behavior, and approximate
   per-second price. If values were omitted, label them as defaults and say the
   user can ask for another listed mode. For prompt mode, show the exact prompt
   in a fenced block, after trimming surrounding whitespace, and ask for explicit
   approval. Do not paraphrase it in the approval message. For clone mode, say
   clearly that no prompt will be sent because motion comes from the source.

6. Animate the approved frame. `generate_reaction_video` with the approved
   `frameIds` and a `mode`. For prompt mode, pass `promptApproved: true` only
   after the approval in step 5. Poll each generation until its state is terminal:
   `succeeded`, `failed` or `canceled`. The clip is `output.url`. (The board in
   `list_reaction_videos` calls the same finished state `complete`; a generation
   never reports `complete`, so a client waiting for that word waits forever.)

7. Hand over. Download and attach every completed video in the chat reply,
   following Delivering assets in chat below. Report the spend and the exact
   generation-specific dashboard link (see Money and link).

## Two ways to recreate a source performance

When a user says “clone,” make the distinction explicit. They have two valid
paths after the first-frame checkpoint:

1. **Exact motion-control clone.** Use `one_to_one_standard` (or
   `one_to_one_clone_premium`) when they want the closest possible one-to-one
   reproduction of the source performance. It needs a frame made from that
   template, takes no prompt, and follows the source clip's duration.
2. **Prompt-directed recreation.** Generate the first frame with any supported
   image model, get it approved, then animate it in a prompt mode (Seedance,
   Grok, PixVerse, or Kling). The caller may supply any motion prompt and choose
   a supported duration. If they do not want to write one, call
   `get_reaction_template` with the source `templateId`. The stored prompt is
   `template.motionAnalysis.prompt`; pass that value to
   `generate_reaction_video` only when `motionAnalysis.status` is `complete`.

Use the first path for faithful motion replication and the second when the
user wants to preserve the source's overall movement while changing duration,
model, or creative direction. Do not paste the short `motion` field from a list
result into `generate_reaction_video`; it is only a browsing summary. The full
analysed prompt is `motionAnalysis.prompt` on `get_reaction_template`. Omitting
`mode` defaults to the prompt family (`seedance_2_0_fast`), so name a clone mode
explicitly when exact motion control is intended.

### Prompt approval is a separate checkpoint

For a prompt-directed recreation, show the exact proposed generation prompt in
a fenced block. When it came from source analysis, also show
`motionAnalysis.timeline` separately as explanatory timing. Ask whether they
approve the exact prompt and timing, or want either changed. Do not pass a prompt
to `generate_reaction_video` until the user explicitly approves it, and never
set `promptApproved: true` speculatively.

This does not replace first-frame approval: after the prompt is approved, render
the frame, show it to the user, and get a second explicit approval before
starting the paid video generation.

### Where the analysis lives

The import pipeline attempts to analyse each source automatically, but an
analysis can be missing while a job is queued, retried, or has failed. The
canonical place to read it is the free `get_reaction_template` response:

```text
template.motionAnalysis.status
template.motionAnalysis.prompt
template.motionAnalysis.timeline
```

Use `template.motionAnalysis.prompt` only when its status is `complete`.
Call `generate_reaction_prompt` only as a repair:

- when `motionAnalysis` is absent;
- when its `status` is not `complete`; or
- when the source was re-cropped or otherwise changed after the analysis was
  written.

It is a write tool and can spend on a vision call, so do not reach for it before
checking the free read.

The same template response also carries the source descriptions:

- `opensOn` is the opening still: camera distance, gaze, hands, light. Prompt
  mode obeys the picture more than the words, so this is what you are really
  choosing when you pick a clip.
- `motionAnalysis` is the timed motion across the whole clip.

`list_reaction_templates` and `list_inspiration_reactions` carry both shortened
to one browsing line. `get_reaction_template` carries both in full.

## Reusing existing work

`list_reaction_videos` is the compact inventory of existing renders. Rows carry
`avatarId` but not the avatar name, so resolve names with `list_avatars` when you
are reporting a board back to the user. A row's `videoUrl` is the canonical clip,
which is the post-edit version once one exists. A row's
`sourceReactionId` identifies the canonical source template; call
`get_reaction_template` to read that source clip, its import/original URL, its
full `opensOn` still description, and its cached motion analysis. Call
`get_reaction_video` only when you need the actual prompt and resolved settings
used for a particular generated render. The template analysis is a starting
point: for prompt-mode generation, use the motion the user actually asks for and
pass that as `prompt`.

`list_reaction_video_modes` has every mode with its per-second cost, so offer the
premium or higher-quality options with prices when the user wants better than the
default.

## Batches

Give `generate_reaction_frames` several avatars and you get one frame generation
each. Poll them together with `list_generations`. After the user approves the
frames they want, pass just those `frameIds` to `generate_reaction_video`. The
user can approve some and have you regenerate others, that is normal. Download
and attach every completed frame separately, label each attachment with its
avatar, and preserve each terminal generation's exact `dashboardUrl`. Never
replace frame-specific links with a generic workspace URL.

## Delivering assets in chat

Whenever a Ghostfeed result contains a finished user-facing asset, download
`output.url` (or the result's equivalent image/video URL) to a temporary local
file and attach or render that local file with the chat host's native media
mechanism in the same reply. This applies to approval frames and finished
videos, including batches. Use the response Content-Type or actual file format
for the local filename, keep the file until the reply has been delivered, and
label each attachment with its avatar or generation.

Do not embed the remote asset URL directly as a Markdown image or video: remote
previews are not reliable across hosts. Preserve the MCP `resource_link` for
open/play/download and the terminal generation's exact `dashboardUrl`. If the
host cannot attach local files, say that the preview is unavailable and provide
that exact asset-specific dashboard link; do not claim the asset was shown and
never substitute a generic workspace URL.

## What stays in the dashboard

You do bulk creation. Everything else is a human-in-the-loop step in the
dashboard: cropping a 30 to 120 second import, renaming or deleting templates and
videos, and editing a finished clip (speed, text overlays, download). Do not try
to do those over MCP. When an import lands `needs_action`, send the user to the
`dashboardUrl` to crop, then continue.

## Workspaces

Call `list_workspaces` first and keep the chosen slug or id. Reads may omit
`workspace` and use the credential's pinned read default. Every write requires
`workspace`; never infer it from whichever workspace the user last opened. A typo
fails with remediation listing the valid names, slugs, and ids.

## Money and link

Importing a template costs nothing. Frame generation reports an
`estimatedCreditCost` and charges as the frames render; video generation reports
the real `creditsSpent` and `creditsRemaining`. When a response carries
`creditsSpent` and `creditsRemaining`, state them on their own line, numbers from
the tool result:

```
💳 {creditsSpent} credits spent, {creditsRemaining} remaining
```

Reads and lists get no money line. `get_credits` has the balance if the user
asks.

When a response carries `dashboardUrl`, end your reply with the door on its own
line:

```
🔗 {dashboardUrl}
```
