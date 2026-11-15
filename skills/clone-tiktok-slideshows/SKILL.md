---
name: clone-tiktok-slideshows
description: Copy the design of another post or deck (a TikTok or Instagram link, a reel, screenshots, an Inspiration pick, or one of the user's own decks) with new pictures, and the same or new words. Use together with ghostfeed-slideshows and ghostfeed-slideshow-taste.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-slideshow-clone` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

Load `ghostfeed-slideshows` and `ghostfeed-slideshow-taste` first: the tools, slide
HTML rules, Finding pictures, the last look and delivery all apply. This
skill adds what a copy needs.

The goal is a deck that looks like it came from the same account: the same
format and design, with new real pictures. The bar is the source itself. Put
the two side by side and the design must be the same. Copy the design
exactly; never reuse the images. Keep or change the words as the user
chooses.

## 1. Get the source

- A link: `import_template_from_social_post` with the url, then
  `get_slideshow_template` with the `templateId` and `waitMs: 25000` until
  `status` is `ready`. It gives the caption and each slide's image url. If
  the import fails, say why in plain words and ask for screenshots of every
  slide. In an MCP Apps host, `render_slideshow_result` with
  `template: { templateId }` shows the post to the user; its Make a
  slideshow like this button sends you a request with that `templateId`.
- An Inspiration pick: its slide image urls and caption come with the
  `search_inspiration_slideshows` result.
- Screenshots in the chat: use them directly. You can see them, so in every
  host compare each render with them yourself; never ask the user to add
  them again.
- One of the user's decks ("same format as my X deck"): `list_slideshows`,
  then `get_slideshow`; reuse its style block and each slide's layout
  exactly.

## 2. Study every slide

Look at each source slide on its own at full size (`analyze_image` with its
url), never a shrunk contact sheet. For each slide, note:
- the canvas shape (Instagram carousels are mostly `4:5`, TikTok `9:16`);
- each text box: font look, weight, italic, case, colour, alignment,
  position, lines and words, and its size in px on our canvas. Measure the
  height of a capital letter as a share of the slide height; font size ≈
  cap height ÷ 0.7. Write the number down and never guess smaller (body on
  photo carousels is usually 34–48 px at 1080 wide, headings 70–120 px);
- every picture: its KIND (photo, drawing or line art, engraving or
  painting, cut-out portrait, screenshot, sticker, none), its width and
  height as a share of the slide, its place and treatment (full-bleed or
  framed, crop, border, radius, shadow, black and white, tint, how dark it
  is behind text);
- every decoration: rules, boxes, highlights, arrows, numbers, tags,
  handles, page dots, logos, stickers, shapes;
- the rhythm: text-heavy slides, quote slides, photo-only or small-caption
  slides, and the ending.
Then pick matching fonts with `list_slide_fonts`.

## 3. Topic

Study the source BEFORE you ask anything. If the user already said what they
want, do that. If not, say in one or two lines what the post is, then ask one
short question with three options (the host's question tool if it has one,
otherwise one short message with the options numbered):
1. The exact same words, with new pictures.
2. and 3. Your two best other ideas for this post, from what it is and why it
   works.

## 4. Build

1. `create_blank_slideshow` with the source's ratio and EXACTLY its number of
   slides (cap 20; above that, merge or drop the weakest beats). Its slides
   start classic; the `write_slide_html` (replace) of each slide below makes
   it an HTML slide.
2. Pictures of the SAME KIND in the same places (Finding pictures, plus):
   - never the source's own images;
   - new subjects, not the source's subjects slide by slide, unless the post
     is about those exact things;
   - drawings, engravings, paintings: search that medium ("pen line drawing
     child crayons", "vintage engraving travellers"); cut-out portraits: a
     real photo of the person in black and white with CSS `filter`;
   - websites and apps: real, well-known ones only; `search_google_images`
     `"<name> website"`, or, in a host with a shell, capture the page yourself
     (wait for it to load, close cookie banners, check the capture) and upload
     it with `request_media_upload`, then `complete_media_upload`. Never name a
     site or app you do not know exists; a pinned design mockup is not a site;
   - stickers and cut-outs: `search_pinterest` `"<thing> sticker png"`;
   - a named person gets a real photo of that person (`search_google_images`);
   - same size and place as the source: a drawing that fills half the
     source slide fills half of yours; a drawing or swatch on the plain slide
     colour shows no paper box (pick a white ground and add
     `mix-blend-mode: multiply` on a light slide);
   - where the source has a picture, the copy has one. When research cannot give
     it, offer to generate it (Finding pictures in `ghostfeed-slideshow-taste`).
     Never replace pictures with CSS doodles unless the source has doodles.
3. Write slide 1, then compare: `render_slides` with `compareWithSourceUrls`
   (source slide 1), or next to the screenshot in the chat. List every
   difference (size, position, font, darkness, picture kind, decoration,
   spacing) and fix it with `edit_slide`. Check
   text size first: compare the height of one body line and of the title; if
   ours is smaller, multiply the font sizes by the ratio. Then each picture's
   width and height. Repeat until nothing visible differs (three rounds at
   most).
4. Write the other slides with the same style block. Keep the rhythm
   exactly: photo-only slides stay photo-only (never black or empty), a
   small-caption slide gets only a small caption, a quote slide stays a quote
   slide.
5. Words: keep what the user wants kept (Understand what you are given, in
   `ghostfeed-slideshow-taste`). When they did not ask to keep the words, write
   your own: keep the structure and beats, change the examples and every
   sentence. Match a source slideshow's amount of text per slide (60 words for
   60, 4 for 4); here the source sets the length, not What makes a deck good.
   Add nothing the source lacks: no labels, kickers, page numbers, footers,
   logos, or "illustrative image" or credit notes. Keep every decoration it has.

## 5. Check and deliver

`render_slides` with `compareWithSourceUrls` (all source slide urls in
order), or with the screenshots in the chat next to it, and LOOK at every
slide. This is required: a copy you have not compared side by side with its
source is not done. Fix every slide that differs and compare again. Then the
caption in the source's voice and length with `set_caption`, and deliver.

## Follow-ups on a copy

Do exactly what the user asks and keep everything else (Editing an existing
deck), plus:
- "Make another one with a new (adjacent) topic", none named: pick the best
  one yourself, say it in one line, and build it. Do not ask.
- "Make another one, same format, about X": reuse the previous deck's style
  block and every slide's layout, with new words and new pictures of X.
- "Same styling, new format": keep colours, fonts, hierarchy and the KIND of
  pictures; design new layouts and still find pictures. A deck about a
  person shows that person on the cover.
- "Make the text as big as the original": compare with
  `compareWithSourceUrls` and scale by the measured ratio.
