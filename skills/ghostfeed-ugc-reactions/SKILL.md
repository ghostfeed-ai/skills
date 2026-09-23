---
name: ghostfeed-ugc-reactions
description: Create and recreate UGC images and videos with Ghostfeed tools. Choose image creation, composition cloning, editing, prompt-directed motion, or Wan 3 reference-guided motion; use Brands, Product images, avatars, and saved source understanding as needed.
---

Translate the user's goal into the necessary tools. A request to “clone this
video” can mean copying its composition, recreating its actions from analysis,
or guiding a new performance with the original media. Choose the relevant parts;
there is no mandatory end-to-end sequence or MCP App wizard.

## Choose the creative operation

| Intent                                                                        | Tool                                                      | Important inputs                                                                                                                  |
| ----------------------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Create an image from an idea or references                                    | `generate_image`                                          | `instruction`; optional `avatarId`, `productImageId`, and `referenceImages`                                                       |
| Recreate a composition with a selected identity                               | `clone_image`                                             | `composition`, required `avatarId`, optional `productImageId` and instructions                                                    |
| Change an existing image                                                      | `edit_image`                                              | `image` and `instruction`; preserves the original                                                                                 |
| Animate from action you write                                                 | `generate_video_from_prompt`                              | `image`, selected `mode`, and `prompt`                                                                                            |
| Guide motion or performance directly with media                               | `generate_video_from_reference`                           | `image`, Wan 3 `mode`, `reference`, and `guidance`                                                                                |
| Read or explicitly request source understanding, or prepare generation action | `get_reaction_template`, then `analyze_video` when needed | Saved `videoUnderstanding` first; `profile: "understanding"` only when missing/failed; model-specific action profiles when needed |

Each creative call produces one output. Several references describe one output;
they are not a batch count. For several requested outputs, submit distinct calls
with distinct idempotency keys and track each generation.

## Workspaces, models, and existing assets

Call `get_me` and `list_workspaces` when establishing context. Pass the chosen
workspace slug or ID explicitly on every write. A Brand name and a workspace
name are different identities; resolve each through its own discovery tool.

Use `list_image_models` and `list_reaction_video_modes` to choose supported model
IDs, reference types/counts, duration, resolution, audio behavior, and prices.
Do not invent models or silently drop incompatible references. When a requested
combination is unsupported, explain the specific constraint and choose an
appropriate alternative with the user.

Reuse a suitable existing image when the user's request permits it. Use
`list_reaction_frames` and `get_image` to inspect it. Changing the video model or
action does not inherently require generating another image. An old frame's
existence does not prove that the user liked it; respect their stated choice and
any request to review the image before proceeding.

For avatars, use existing avatar discovery and creation tools. Load the
`ghostfeed-avatars` skill when creating a new identity; its approval rules remain
unchanged. Do not create a new avatar just to change a scene or garment.

## Brands and Product images

- `list_brands` / `get_brand` find saved marketing context and processing status.
- `create_brand` creates a Brand from website information or explicit details.
  Website enrichment and Product image harvesting are asynchronous; inspect
  `get_brand` rather than assuming the images are ready immediately.
- `update_brand` changes supported details.
- `list_product_images` returns the Brand's directly owned Product image IDs.
- To add files to a Brand, call `request_product_image_upload`, PUT bytes to its
  signed URL with the returned Content-Type, then call `add_product_images` with
  the returned upload keys and filenames. Repeat the same ordered inputs when
  retrying completion. Generic media uploads are a separate reference path.
- Rename or remove a Product image only as requested, using the corresponding
  Product image tool. Collections are not required for UGC product references.

`clone_image` selects the product-aware default whenever `productImageId` is
supplied. It inserts that product even when the composition has none, allowing
necessary pose/hand/placement changes while preserving avatar identity and
product appearance. Template + product cloning without an avatar is unsupported.
For product-only scenes, use `generate_image` with instructions and supported
references instead.

## Source videos and uploads

Use the source the user supplied or selected. When the request needs a source
and none was supplied, discover appropriate sources with `list_reaction_templates` and `list_inspiration_reactions`. Library
`firstFrameScene` and the saved `videoUnderstanding` help selection. Older rows
may expose `opensOn` and `motion` summaries instead; those are not full action
prompts.
Import a social link or inspiration into the workspace with
`import_reaction_template` when a saved template is needed. Poll its generation.
Long completed imports remain usable. Crop only when the chosen generation workflow
needs a shorter or cleaner reference range; `render_source_crop` supports visual
selection in an Apps host.

### Choose the part to recreate

After importing a source for cloning, establish which part the user wants before
preparing generation. A long organic video often combines a short creator hook,
a product demo, and sometimes a creator return. Do not assume the entire clip is
the intended motion reference. If the request does not already identify the part,
ask one concise question: the opening hook, the creator parts, or the whole video?
Respect an explicit selection; do not ask again or force a hook-only workflow.

Read `get_reaction_template` for source media, duration, and `videoUnderstanding`.
Imports create understanding at no user credit cost and remain processing until it
completes. Its saved
result contains `understanding.firstFrameScene`, `generationPrompt`,
`description`, `contentStructure`, `demoType`, simple timestamped `sections`,
and optional visual format, editing complexity, and approximate transcript.
New cropped templates are exact media assets with their own
understanding and crop-relative timestamps. Historical crops may also carry
`sourceContext` for the whole original and `range` for the selected source interval.
Use the cropped asset's sections to identify the requested part; whole-source
categories remain supporting context and never restrict generation.
Cropping a template currently starts a new understanding job for that cropped
asset. The crop generation can succeed before that analysis finishes: read the
new template and wait for its understanding to complete before using its
crop-specific descriptions or generation prompt. Do not call `analyze_video` again for
the same crop unless its saved understanding is missing or failed and the user
requests a retry. The new analysis describes the crop's actual first frame and
action; the whole source's first-frame scene and generation prompt must not be
presented as facts about a later segment.

If understanding is absent on an older template, call `analyze_video` with
`profile: "understanding"`; this explicitly enrolls that template in the same saved
analysis lifecycle. For `pending` or `processing`, wait briefly and poll the
template read or the same analysis request; both reuse the saved job. For `failed`,
explain that analysis failed and use `retryFailed: true` only when a retry is
explicitly requested. Do not loop retries. A new import remains unavailable
until its understanding succeeds; older completed templates without this analysis
retain their established generation fallback. The 120-second import limit still applies.

Sections and transcripts are approximate, not verified cut points or subtitles.
When a boundary matters for motion control, inspect the source or use
`get_source_frame` near the transition and confirm the crop preview. A still
frame cannot verify speech or lip-sync. Do not invent timestamps. If the result
and visible footage disagree, use the footage and explain the uncertainty.

- **Reference-guided motion:** isolate the selected source range with
  `crop_reaction_template` when the reference includes unwanted demo or other
  footage. Use the user's supplied/approved range, poll completion, and pass the
  new template ID as the reference. Keep source audio aligned to the same range.
  An exact Crop request from the Apps selection authorizes that crop: use its
  supplied source and start/end times without asking for the same approval again.
  Use saved understanding and source inspection to choose one continuous range
  containing the complete requested part. This creates one clip, not an automatic
  collection of scene clips.
- **Full-length reference clone:** when the user wants the whole source and a
  selected model limits reference duration, plan an ordered set of adjacent
  ranges that covers the requested interval. For Wan 3 Video Guided, each source
  reference must be at most 15 seconds. Wan 3 outputs use whole-second durations
  from 2 to 30 seconds; for a faithful clone, plan each range near a supported
  whole-second length and set `durationSeconds` explicitly to that range's
  intended output length on **every** `generate_video_from_reference` call.
  Omission produces the five-second model default, even for a longer crop.
  If a natural boundary leaves a fractional duration, adjust a nearby cut when
  the footage allows it, or explain the duration mismatch before generation.
  Place boundaries at natural changes in movement or scene, not mechanically
  at 15-second marks. Use the original
  understanding to propose boundaries, then inspect nearby source frames and
  the crop preview; its timestamps are approximate. Avoid an impractically
  short final range by adjusting an earlier boundary. Crop each range from the
  original source, poll each crop generation, and use its own starting frame/composition
  for the selected avatar. Generate one video per crop in source order, with
  separate idempotency keys. Do not silently switch to another model or offer
  one 15-second reference as a faithful clone of a longer performance. Price
  the complete plan, including any additional starting images, before paid
  generation. The outputs are independent takes: inspect transitions and do
  not promise seamless motion or audio. MCP currently has no video-stitching
  tool; provide the dashboard editor link for assembly and say clearly when
  the requested final combined video has not yet been delivered.
- **Prompt-directed recreation:** read the source understanding, then write the
  `prompt` for only the selected section yourself. The backend does not write or
  insert the source's saved generation prompt for this tool. Cropping the
  original is unnecessary when only written action guides generation. If there
  is not enough evidence to write that action, resolve the missing detail
  before generation.
- **Demo footage:** ask for or reuse the user's own product demonstration when
  it is needed in the result. Do not copy the source app's interface or present
  invented functionality as the user's product. A hook-only request needs no
  demo. For assembly beyond generation, provide the dashboard editing link.

These choices also apply to animation and other source formats. A category helps
interpret the footage; it does not decide what can be generated or override the
user's goal.

For local Image, Video, or Audio references:

1. `request_media_upload` with filename, Content-Type, byte length, and a stable
   upload ID when retrying.
2. PUT the bytes to the returned signed URL using its Content-Type.
3. `complete_media_upload` with `uploadId`. Use the returned `mediaId` thereafter.

An upload URL alone is not a usable reference. Completion validates media and
stores an immutable accepted asset with server-measured audio/video duration.

Sources for analysis use **exactly one** of
`{ "templateId": "..." }`, `{ "mediaId": "..." }`, or `{ "videoId": "..." }`
for a completed generated video in the selected workspace. Reuse that video ID
directly; downloading and reuploading the generated video is unnecessary.
Frame extraction accepts only `{ "templateId": "..." }` or `{ "mediaId": "..." }`.
`get_source_frame` accepts `source` and `timestampSeconds` and returns a saved
`frameId`. It works directly on completed uploaded videos; template import is
not required. Repeating the source/timestamp reuses the saved frame. Audio-only
uploads cannot supply an image frame or visual action analysis.

Image references use explicit kinds, for example
`{ "kind": "frame", "frameId": "..." }` or
`{ "kind": "upload", "mediaId": "..." }`. Use returned IDs rather than inventing
URLs or translating one kind of ID into another.

## Images and composition

`generate_image` supports text-only creation and multiple references without an
avatar when the selected model supports them. For identity or product-led
creation, supply the corresponding IDs and a concise scene instruction.

`clone_image` accepts a template, saved frame, or completed uploaded image as
`composition`. It requires an avatar and automatically chooses the applicable
clone default. To copy a specific moment in a video, first obtain its saved
frame with `get_source_frame`, then use that frame as the composition.

`edit_image` makes a new image from a saved frame or completed uploaded image and
a requested change. The edit default preserves unrequested content. Follow the
user's requested review checkpoints; the tools do not require presenting every
system prompt before execution.

## Two ways to recreate a video

### Action described by a prompt

Use `generate_video_from_prompt` when written action controls the result. Supply
the complete `prompt` yourself. For a source recreation, read its saved
`videoUnderstanding` and inspect the requested section, then write a prompt for
that result. The saved `generationPrompt` is context, not text the backend
silently submits. For older sources without understanding, use `analyze_video`
to obtain source context. If the user supplies an exact prompt, preserve it.

The source supplies action text; this does not automatically make its video a
motion-control input. The starting image's composition source and the action
source can differ. Your prompt must not inherit unrelated source movement.

### Performance guided by reference media

Use `generate_video_from_reference` when motion Video or Audio directly guides
the output. A completed generated video can be the `reference` as
`{ "videoId": "..." }`; in the additional `references` array use
`{ "kind": "video", "videoId": "..." }`. Supply the starting image and explicit `reference`; it does not need
to be the image's original source. Existing motion-control modes are
`one_to_one_standard` and `one_to_one_clone_premium`. Their supported input and
duration rules come from the catalogue; do not promise identical generated
pixels or unrestricted duration control.

For direct video cloning, recommend **Wan 3 Smart Motion — Video Guided** by
default: `generate_video_from_reference` with `mode: "wan_3"` and
`guidance: "video_guided"`. Check its reference limits and pricing first. Respect
an explicitly selected model; when Wan 3 cannot support the requested input,
explain the constraint and choose a supported crop or alternative with the user.
For audio-led performance, use Wan 3 Smart Motion — Audio Guided when appropriate.

Use dashboard model names in conversation: **Kling 2.6 Motion Control** maps to
`one_to_one_standard`; **Kling 3 Motion Control** maps to
`one_to_one_clone_premium`. These are compatibility IDs, not user-facing tier names.
Do not describe these models as “1:1 Standard” or “1:1 Clone Premium”.

For “clone this video,” select the family that fits the user's requested result.
Prompt recreation suits adapting the action. Reference guidance suits directly
following source motion/performance. Ask about this difference only when it
materially changes the intended result and the request does not resolve it.

For a visible lip-sync performance to an existing sound, prefer supported
video-guided motion when the user wants to keep that performance. Use a clean
reference range and preserve the matching original audio when the selected
mode supports it; check the catalogue's actual audio behavior. A transcript is
context, not a replacement for the sound's delivery and timing. Music under
silent reactions or B-roll does not establish lip-sync. If overlays obscure the
performance, obtain a usable reference or explain the limitation. Do not promise
exact mouth synchronization. New words or a new voice may need a different path.

## Prompt-directed H3 and reference-guided Wan 3

| Dashboard choice                  | Tool                            | Parameters                                  |
| --------------------------------- | ------------------------------- | ------------------------------------------- |
| H3                                | `generate_video_from_prompt`    | `mode: "minimax_h3"`                        |
| H3 Max                            | `generate_video_from_prompt`    | `mode: "minimax_h3_max"`                    |
| Wan 3 Smart Motion — Audio Guided | `generate_video_from_reference` | `mode: "wan_3"`, `guidance: "audio_guided"` |
| Wan 3 Smart Motion — Video Guided | `generate_video_from_reference` | `mode: "wan_3"`, `guidance: "video_guided"` |

Do not recommend H3 Smart Motion for new work. Its guided modes remain accepted
temporarily for compatibility with existing clients and saved setups. Use H3 or
H3 Max for prompt-directed action and Wan 3 for new audio/video-guided work.

Both Smart Motion choices use one starting image plus one guidance source.
Do not attach extra product images to guided modes; incorporate the product into
the starting image first if needed. Ordinary H3 has its own additional-reference
capabilities, and H3 Max has its own model settings.

**Audio Guided:** the reference may be Audio or a Video whose audio the backend
extracts. Video sources receive the appropriate audio-guided action preparation.
Audio-only sources do not require visual analysis or a custom action prompt.
Use the supported output duration. Duration-dependent action preparation is refreshed
only for legacy templates or direct media that lack a saved canonical generation prompt.

**Video Guided:** supply a Video reference. Wan 3 Video Guided uses the
inspectable `wan3-video-guided` system prompt by default, but needs no custom
action prompt: the starting image and source video carry identity and motion.
Do not analyze or write an action prompt unless the user asks to change the
source performance. For H3 Video Guided, new template imports reuse their canonical
provider-authored generation prompt; older templates and direct uploads fall
back to motion-prompt analysis. Reference input duration can affect cost.
For either guided choice, `actionPrompt` can explicitly specify the action and
`adaptation` expresses requested changes.

Read `get_prompt_template` with `wan3-video-guided` to inspect or edit Wan 3's
default system guidance before generation when needed. Passing `systemPrompt`
replaces that default exactly; `null` removes it. The submitted system text is
saved in `get_generation_prompt`. Other public guided modes do not receive a
default system prompt.

## Analysis and prompt transparency

`analyze_video` has two purposes. `understanding` reads or explicitly starts the
free, asynchronous saved section analysis described above. For templates it uses
the same canonical record returned by `get_reaction_template`. Generation action preparation is
optional: choose `standard`, `audio_guided`, or `video_guided`; audio-guided
analysis requires `outputDurationSeconds`. The generation tools use the same
preparation automatically when source-derived action is requested.

Keep these distinct:

- An image's saved generation prompt.
- A source video's factual understanding, section map, and provider-authored
  generation prompt.
- A legacy source video's fallback motion-prompt analysis.
- Any explicit caller-supplied system guidance.
- The final submitted prompt and reference order.

A frame may link to a source without storing an independent video action prompt.
Use `get_image` for lineage. Do not substitute today's analysis or defaults when
claiming to reproduce a previous generation's actual settings.

The MCP adapter never invents a system prompt. Wan 3 Video Guided selects its
inspectable backend default unless the caller overrides or removes it. Submitted
system text is saved and can be inspected using `get_generation_prompt`.
Retrieve saved nonbilling settings with `get_generation_setup`. Historical
unavailable fields are not permission to invent missing settings.

## Jobs, retries, and delivery

- Agree on the proposed paid work and its estimated cost or a scoped budget
  before submitting it. Permission to import, inspect, or test is not permission
  to spend on additional analysis or generation. Respect an already approved
  scope and ceiling; ask again before expanding them. A retry is not permission
  to pay for a new output.
- Supply a stable `idempotencyKey` before each paid request. Retry the identical
  request with that same key after a transport failure. A changed request or a
  deliberately new output needs a new key. If preparation ends with
  `preparation_expired`, the same key preserves that failure. Create a new key
  only for an explicitly requested retry, rather than repeatedly resubmitting.
- Poll the returned generation ID with `get_generation`. Use the returned
  status and error information; do not resubmit merely because preparation or
  rendering is slow. Generation success is `succeeded`, not the board's
  `complete` label.
- Use model pricing and `maxCredits` when a budget ceiling matters. Report
  actual credits from returned data, not a guessed amount.
- Show images with `render_image_results`, videos with `render_video_result`,
  and history with `render_generation_gallery` in MCP Apps hosts. Use the
  supplied IDs, URLs, and generation-specific dashboard links. Apps support
  inspection and choices; the agent decides the creative workflow.
- Apps buttons may send contextual, open-ended chat requests containing the
  selected asset and its saved context. Treat a Reference or Recreate selection
  as the starting point for the conversation: inspect the supplied context and
  ask only for creative intent that is still missing. Reuse existing answers and
  explicit instructions; do not make the user restate them. Selecting an asset
  does not itself approve paid generation. Follow the user's existing spending
  authorization and review preferences before a paid tool call.
- Without App rendering, use the returned media and dashboard links. Do not
  claim an asset was generated or visually checked before it is available.

Legacy reaction generation calls remain available during migration. Their
notices name the replacement process and the October 15, 2026 retirement date. Use the
new intent tools for new work; never repeat a successful paid legacy generation
just to migrate its call. Slideshow workflows, finished-video editing, and
publishing are outside this skill's UGC generation scope.
