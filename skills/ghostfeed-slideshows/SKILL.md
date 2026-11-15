---
name: ghostfeed-slideshows
description: Design and build TikTok and Instagram photo slideshows as the art director. Every slide is HTML and CSS you write, rendered by Ghostfeed's server so you see exactly what will post. Build from an idea, edit a deck, cast the user's own Brands, collections and avatars, and make variants. Refined from real founder dogfooding.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-slideshows` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

Every slide is a fixed canvas that you design with HTML and CSS. Ghostfeed's
server cleans what you write, gives every element a `data-id`, renders the
slide in a real browser and hands the picture back to you. The user can open
the deck in the Ghostfeed editor, drag and retype anything you made, and
exports exactly what you saw. You are the designer: there is no fixed list of
templates or layouts. If you can draw it with HTML and CSS, you can make it.

**Copying a design?** When the user wants the design of another post or deck
("copy and create this", "make one like this", a TikTok or Instagram link,
screenshots of a slideshow, "same format as my X deck", or an Inspiration
pick), also load the `ghostfeed-slideshow-clone` skill (`get_skill`) and
follow it. It uses everything in this skill.

**Always also load `ghostfeed-slideshow-taste`.** It decides what is good: what the
user really wants, the look, the pictures, the words, and the last look
before you deliver. This skill says how to build it.

Everything else starts here: build from an idea (Building from an idea), edit
a deck (Editing an existing deck), or make a variant (Variants).

## The tools

Fill every input exactly from the tool's schema; a wrong key fails the whole
call. Every write needs `workspace` (Workspaces and questions). The basics:
- `create_blank_slideshow` makes the deck, at most 20 slides, in `9:16`
  (default), `4:5`, `3:4` or `1:1`. Pick the name, shape and slide count
  yourself when the user did not say. Its slides start as
  classic slides; the first `write_slide_html` (mode `replace`) on a slide makes
  it an HTML slide. Build every new deck that way. Once a deck has an HTML
  slide, `add_slide` adds HTML slides.
- `save_slide_asset` saves a picture; only its `gf://asset/<id>` ref can go on
  a slide. Free.
- `list_slide_fonts` lists the font families slides can use, with their
  weights. Use the exact names. `TikTok Sans` is TikTok's own caption font.
- `write_slide_html` writes a whole slide (`replace`), or adds one group of
  elements to it (`insert` with `parentId`, `null` for the slide root, and
  `index`).
- `edit_slide` changes a slide by element `data-id`, many ops in one call, all
  or nothing: `set_style` (`null` removes a property), `set_text`, `replace`,
  `insert`, `remove`, `move` and `set_attr`.
- `render_slides` shows the saved slides, up to 20 at once, next to the source
  when copying (`compareWithSourceUrls`: SOURCE left, OURS right). Free.

Every write returns the canonical `html` and the render as an image. After
every write, look at the render. That picture is the truth.

## Writing slide HTML

- Write the slide's contents only: no `<html>`, `<head>` or `<body>`. The
  slide root is already the canvas size, `position: relative` and clips at
  its edges. Lay out in CSS px against the canvas `width`/`height`.
- One `<style>` block at the top of a slide is fine. Put the deck's design in
  it as classes (`.title`, `.kicker`, `.photo-frame`, `.caption`) and use the
  same block on every slide of the deck. That block is the deck's format: the
  same classes with new words and photos make every slide match.
- Images only from `save_slide_asset` refs. Scripts, event handlers, iframes,
  forms and outside urls are removed. Fonts only from `list_slide_fonts`.
- Make it easy for the user to edit by hand:
  - Put each text box in its own element (`<h1>`, `<p>`, `<div>`), with the
    words as real text. Style single words inside it with `<em>`, `<strong>`
    or `<span style="...">`. Never draw text with `::before`/`::after`
    `content`, and never put text inside an image.
  - Mark a full-slide photo or colour layer with `data-role="background"`.
    The editor locks it so the user cannot drag it by accident.
  - Keep layers flat: text boxes and pictures are direct children of the
    slide. Never wrap the whole slide in one full-size box; put the slide
    colour on its own `data-role="background"` layer.
  - Give important layers a short `data-name` ("Hook", "Photo", "Logo").
  - Prefer absolute positioning (`position: absolute` with `left`/`top` and a
    `width`) for text boxes and photos. Flex or grid columns are fine for
    stacks and grids.
- Draw decorations with CSS, not images: lines, boxes, highlights, gradients,
  shapes, sticky notes, colour swatches, arrows, frames, tape, stamps, "pills".
  `border`, `border-radius`, `box-shadow`, `linear-gradient`,
  `radial-gradient`, `transform: rotate()`, `clip-path`, `mix-blend-mode`,
  `filter`, `backdrop-filter`, `text-shadow`, `-webkit-text-stroke` and CSS
  grid all render.
- Emoji render (Noto Color Emoji).
- On 9:16, keep text out of TikTok's UI: the top 270px, the bottom 280px, and
  in the lower half the right 180px and the left 100px (at 1080 wide). On 3:4,
  4:5 and 1:1, keep 12% of the height clear at the top and bottom. This is
  guidance; the user may want text there.

### The Ghostfeed kit (optional)

A small stylesheet is always loaded. Every rule has zero specificity, so
anything you write wins. Use it for the classic TikTok text look; write your
own CSS for everything else.

- Text: `gf-text` plus a size, `gf-heading`, `gf-subheading`, `gf-body` or
  `gf-cta` (sized for the canvas, TikTok Sans bold).
- The six TikTok text styles, coloured by `--gf-color` (contrast is worked out
  for you): `gf-plain`, `gf-stroke` (outlined, reads on any photo),
  `gf-background` (a rounded box behind every line; put the words in one inner
  `<span>`), `gf-switch`, `gf-background-alt`, `gf-plain-alt`. Example:
  `<p class="gf-text gf-body gf-background" style="--gf-color:#FF3B5C"><span>words</span></p>`.
- Layout: `gf-cover` (an `<img>` that fills the slide, `object-fit: cover`),
  `gf-shade` (a dark layer, strength `--gf-shade`, 0 to 0.4),
  `gf-safe` (a box inside the safe area), `gf-stack-top`, `gf-stack-center`,
  `gf-stack-bottom` (a centred column inside the safe area).
- The editor's text panel applies these same six styles, so text that uses
  them stays easy for the user to restyle.

### Collage layouts (before/after, comparisons, "3 ways to")

The editor's Layout tool has four presets, and you use the same structure so
the user can switch or refill them by hand: Single, 2-up (two rows), 3-up
(three rows) and Grid (2×2). Write the photo area as one locked container
with one cell per photo, in reading order, no gaps:

```html
<div data-role="background" data-name="Layout"
     style="position:absolute;inset:0;display:grid;grid-template-columns:minmax(0,1fr);grid-template-rows:repeat(2,minmax(0,1fr));background-color:#111">
  <img data-slot="cell-1" data-name="Photo 1" src="gf://asset/<id>" alt=""
       style="display:block;width:100%;height:100%;min-width:0;min-height:0;object-fit:cover">
  <img data-slot="cell-2" data-name="Photo 2" src="gf://asset/<id>" alt=""
       style="display:block;width:100%;height:100%;min-width:0;min-height:0;object-fit:cover">
</div>
```

3-up: `grid-template-rows:repeat(3,minmax(0,1fr))`. Grid: both columns and
rows `repeat(2,minmax(0,1fr))`. Single is one `<img class="gf-cover"
data-role="background">`. Put text and other layers after the container.
Use a free design instead when the source's collage is not one of these.

## Building from an idea

1. Orient a new user in one line: you design each slide yourself and they
   can change any slide, by hand in Ghostfeed or by asking you.
2. Read the brief, ask the look question if needed, and plan the deck
   (`ghostfeed-slideshow-taste`).
3. `create_blank_slideshow`, then find and save the pictures (Finding pictures
   in `ghostfeed-slideshow-taste`, and Casting the user's own images below).
4. Write slide 1 with one `write_slide_html` (replace): the picture, then
   the text. LOOK at the render, list what is wrong and fix it with
   `edit_slide` by `data-id`. Do not rewrite the whole slide to change one
   thing.
5. Write the other slides the same way, one `write_slide_html` (replace) per
   slide, so every slide becomes HTML; slides are independent, so write
   several at once when your host allows it.
6. The last look (`ghostfeed-slideshow-taste`), then `set_caption` and deliver
   (Delivering).

## Editing an existing deck

- Find it with `list_slideshows` (filter with `query`), then `get_slideshow`
  with its `variantId` for each slide's html and ids. Edit by those ids;
  never by slide number.
- Read a big deck a few slides at a time. `get_slideshow` without `variantId`
  lists each variant's `slideIds`; then read with `variantId` and about 4
  `slideIds` per call. A read that is too large fails and nothing is cut:
  read fewer `slideIds`.
- Do exactly what the user asks and keep everything else as it is. Small
  changes go through `edit_slide`: move or resize (`set_style` on
  `left`/`top`/`width`), restyle (`set_style`), new words (`set_text`), new
  photo (`save_slide_asset`, then `set_attr` `src` with the new ref), remove,
  add one element (`insert`). Then LOOK at the render; a change you cannot
  see in the render is not done.
- "Change this image to this": save the new picture with `save_slide_asset`
  and `set_attr` `src` on that photo only. A photo the user dropped into the
  chat needs a url first (Casting the user's own images).
- "Add N slides": `add_slide` with `count` (or `copyFromSlideId`), then write
  each new slide in the deck's style block.
- A change to the deck's design (font, colour, a decoration): change the
  style block on EVERY slide the same way, so the deck stays consistent.
- The user may have edited slides by hand. Read the current html first and
  keep their changes unless they ask otherwise.
- `update_slideshow` renames the deck, changes its aspect ratio (every slide
  renders again at the new size; check them with `render_slides` and fix the
  layout), or links it to a Brand.
- `delete_variant` and `delete_slideshow` only when the user asks for exactly
  that. A deck always keeps at least one variant.
- Older decks may have classic slides (Classic slides below).

## Variants (A/B versions of a deck)

`create_variant` with the `sourceVariantId` returns a COPY of that deck as a
new `variantId` with new slide ids (the html and its element ids are
copied). Edit the NEW variant, never the source:

- Keep the design (the style block) unless the user asks for a new one.
- New words: `set_text` on the same text elements, same beat, new words.
- New photos: a different pick of the same kind (a new Pinterest search
  result, another photo from the same collection or avatar). Keep uploaded,
  pasted-url and AI-generated images as they are.

A variant costs 1 credit at `create_variant`, the same as a dashboard variant.

To put an existing variant under another slideshow, use `move_variant`; never
rebuild it. If it is the last variant, say first that its old slideshow will
be deleted.

## Inspiration

`search_inspiration_slideshows` finds proven slideshows from our catalog, sorted by real
engagement, with their slides and captions. Use it when the user wants
"something that works" or names a format, then copy the best one's design
with the user's topic (load `ghostfeed-slideshow-clone`). Use the search words,
category, length and sort the request implies; `list_inspiration_filters` has
the categories and lengths. In an MCP Apps host, show the results with
`render_inspiration_browser` (`media: "slideshows"`, the same search).

## Casting the user's own images, products, and avatars

When the user says "my avatar", "our app", "our product", "our brand" or "my
photos", go to these tools first. Do not ask them to upload or paste an image
their workspace already has. Every pick goes through `save_slide_asset`; put
the returned `ref` on the slide.

- Avatars: `list_avatars` for saved identities. If there is one, use it; if
  there are several and the brief does not name one, ask which. Then
  `list_avatar_images` to browse that avatar's photos and save one with
  `source: { type: "avatar", avatarId, url }`. Use a different photo per
  slide.
- Collections: `list_collections`, then `list_collection_images`, then
  `source: { type: "collection", collectionId, url }`. To make or fill a
  collection, load `ghostfeed-collections`.
- Brands (an app, product, company or store the user names): `list_brands`
  and match the name loosely ("snap list" is the Brand "SnapList"). Then
  `list_product_images` with that `brandId` and save one with
  `source: { type: "brand", brandId, imageId }`. Check Brands before
  collections when the user names a product or app. Plug it on ONE slide in a
  soft peer-recommendation voice, unless the user asks for a promo deck. To
  make or change a Brand, load `ghostfeed-brands`.
- Pinterest: `search_pinterest` returns urls; save a pick with
  `source: { type: "pinterest", url, query }` (the query that found it).
- Google Images: `search_google_images` returns urls; save a pick with
  `source: { type: "url", url }`.
- The user's own file, or a photo they dropped into the chat, that must go
  on a slide (it has no url you can save):
  - In an MCP Apps host, open `render_upload`. When the upload is done you
    get the file's stored `url`; save it with `source: { type: "url", url }`.
  - In a host with a shell, `request_media_upload` gives a short-lived
    upload url; PUT the raw bytes to `uploadUrl` with that `Content-Type`,
    then call `complete_media_upload` with the `uploadId` and save the `url`
    it returns with `source: { type: "url", url }`. It takes JPEG, PNG or
    WebP: convert a GIF or AVIF to PNG or WebP first.
  - Never pass image bytes as a tool argument. Any other public HTTPS image
    url works with type `url` too.
- Logos, product shots, app screenshots and stickers are normal `<img>`
  elements placed on top of the photo; size and position them with CSS.
  An app screenshot is never the slide's background: show it as a phone or
  card about 60% of the slide width on the photo, with the text outside it.

## Generating images

Use this when the user asks for generated images, or agrees to them when
research cannot give the deck what it needs (`ghostfeed-slideshow-taste`:
Finding pictures).

1. Find the avatar: `list_avatars`, match the name the user said, and keep its
   id. If several avatars match, ask which.
2. Decide which slides need a generated image: every slide that shows the
   person, one image per slide. A text-only, product, or Brand slide keeps its
   normal source.
3. Model and price: use the model `list_image_models` marks `recommended: true`
   for `reference_to_image` unless the user asks for another; read that list for
   what each model offers and its current price. Before starting, say the model
   and the total ("6 images with <model name>, 12 credits"). For more than 4
   images, ask first and wait for a yes.
4. Start them all at once, in parallel: one `reference_to_image` per slide,
   each with `references: [{ "type": "avatar", "id": ... }]`,
   `settings.aspectRatio` closest to the photo's frame on the slide (`9:16` for
   a full TikTok slide, `1:1` on a square deck; `list_image_models` lists each
   model's ratios), the model, and an `idempotencyKey` per slide (for example
   the slide id; use a new key only for a deliberate redo). Write a vivid
   `prompt` for that slide's beat: the place, the action, the framing, the
   light and the mood, as a candid phone photo of the person in the reference,
   with no text, captions, or logos in the image. Match the slide's copy; vary
   the setting and light across the deck.
5. Wait for the images in every host: `get_generation` with the
   `generationId` and `waitMs: 25000` for each image, in parallel. It returns
   as soon as the image is done; if it is still `queued` or `running`, call it
   again. These pictures are for the deck, so do not show them with
   `render_image_results`. Never resubmit a generation and never poll in a
   quick loop.
6. LOOK at every finished image (`analyze_image` if you cannot see it). Wrong
   face, broken hands, or baked-in text: regenerate only that slide once, then
   tell the user. A `failed` generation is refunded; say so in plain words and
   use another source for that slide.
7. Save each finished image with `save_slide_asset` and
   `source: { type: "generation", generationId }`, then put its `ref` on the
   slide (`write_slide_html`, or `edit_slide` `set_attr` `src` on the photo).
   Using it costs nothing beyond the deck's normal first-edit credit.
8. Never paste generation links or raw image URLs as the result; the deck is
   the delivery.

## Classic slides (older decks and existing integrations)

`get_slideshow` shows each slide's `kind`: `html`, or `fabric` for a classic
slide. Classic slides come from `create_blank_slideshow` before you write
them, from older decks and from other integrations. Never build a new deck
with them. When you meet one in an existing deck, either:

- rewrite it with `write_slide_html` (replace), which makes it an HTML slide.
  Do this when you redesign it or the rest of the deck is HTML; or
- make a small change with the classic tools: `set_slide_texts` (texts by
  `id`; `x`/`y` are the box centre in canvas px), `set_slide_background` (an
  `image` source with its `query` for Pinterest, `color`, `shade` 0 to 0.4,
  `transform`), `set_slide_images` (logos and stickers on top) and
  `set_slide_layout` (`2up`, `3up`, `4up`, or `single`).

The classic tools refuse HTML slides (the error names `edit_slide`), and each
call saves all or nothing: a background pick under 720px on the short side
rejects the whole call. `render_slides` cannot show a classic slide without a
current render (it lists it in `unrendered`), so check the saved state in the
returned `committedVariant`, and tell the user they can see that slide in
Ghostfeed.

## Saved state and failures

- Use the exact ids each result returns: `slideshow.id`, `variantId`,
  `slideIds`, and the element `data-id`s in the last returned `html`. Never
  guess ids or reuse them from memory after the deck may have changed (the
  user may be editing by hand while you work).
- `edit_slide` is all or nothing: if one op is invalid or names a missing
  `data-id`, nothing is saved and the error names it. Read the slide again,
  fix the op and resend.
- `warnings` tell you what the server changed or could not do (a removed url,
  an unknown font, an unsafe property). Read them and fix the cause.
- If a tool reports missing storage configuration, credentials or
  authorization, stop the affected calls. Changing the input will not fix it.
  Keep what already saved, report the blocker once, and deliver what you have.
- If a slide cannot render, say so plainly. Never say a slide is done when its
  write failed.

## Workspaces and questions

Call `list_workspaces` first. If it returns one workspace, use it without
asking. With several, use the one the user named; otherwise ask once. Pass its
slug or id as `workspace` on every write. Reads may leave it out.

When you need to ask the user something (the look, which avatar, a topic), use
the host's own question tool if it has one. Otherwise ask in one short message
with numbered options. Put everything you need in that one ask.

## Delivering

You are in an MCP Apps host when the product you run in shows MCP widgets in
the chat: claude.ai and the ChatGPT app do; Claude Code, Cursor and Codex do
not.

- In an MCP Apps host, deliver with `render_slideshow_result` and the
  `slideshowId` (and the `variantId` when you made a variant). Call it once
  when the deck is done, and again after changes the user asked for; not after
  every slide. Each card shows one variant. To show another variant, call
  `render_slideshow_result` again with that `variantId`; after New variant,
  show the new variant in its own card. The card shows each slide's server
  render, the exact picture that exports (a slide still rendering says
  "Rendering…" and fills in by itself; a classic slide without a render shows
  a composed preview), the caption, and Open in Ghostfeed for editing by hand
  and publishing. Its full screen view adds Download, Download all, Edit slide
  and New variant. Then summarize the deck in a sentence or two; do not
  describe it slide by slide.
- The view's Edit slide and New variant buttons send you a request that names
  the slide or the variant and the tool to use. Ask what should change if it
  does not say, then work as in Editing an existing deck or Variants. A
  button press is not a yes to spend.
- Without App tools, summarize the deck in two sentences and give its exact
  `dashboardUrl`, where the user can see, edit, download and publish it.

Never present search candidates, source images or asset urls as the finished
deck.

## Price

The blank deck is free; the first successful content edit on it costs 1
credit and later edits are free. When a response carries `creditsSpent` and
`creditsRemaining`, put them on their own line at the end of your reply,
numbers from the tool result:

```
💳 {creditsSpent} credits spent, {creditsRemaining} remaining
```

Reads and free calls get no money line. `get_credits` has the balance if the
user asks.
