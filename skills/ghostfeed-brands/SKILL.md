---
name: ghostfeed-brands
description: Create and edit Ghostfeed Brands. Make a Brand from a website or a name, change its details, add products from a link, and add, rename or remove its images.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-brands` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

A Brand is an app, product, company, or store that the user promotes. Use
these tools when the user asks to make a Brand, change it, or add images or
products to it. All of them are free.

## Before you start

- Call `list_workspaces` once. If it returns one workspace, use it without
  asking. If there are several, ask which one. Pass that `workspace` on every
  write. A workspace is not a Brand: resolve Brand names with `list_brands`.
- To ask the user something, use the host's own question UI if it has one.
  Otherwise ask in one short message.

## Make or change a Brand

- Check first: `list_brands` and match the name loosely. If the Brand exists,
  edit it. Do not make a second Brand with the same name. If `create_brand`
  fails or you do not know if it saved, call `list_brands` before you try
  again.
- `create_brand` works the same as the dashboard. Send a website `url`, or a
  `name` and a `description`.
  - With a website, send only `url`. In the background the server reads the
    name, the description, and the images on that page: the pictures on a
    website's homepage, or every screenshot and the icon of an App Store or
    Google Play app. It adds no products.
    `enrichmentStatus` and `imageHarvestStatus` can be `pending` at first.
    Check `get_brand` once before you reply; do not call it again and again.
    Do not say the images are ready before `imageHarvestStatus` is `ready`. If
    a status is `failed`, say so in plain words.
  - Without a website, send the `name` and a one or two sentence
    `description` in the user's own words. If the user gave you nothing to
    describe it, ask one short question.
- `update_brand` with the `brandId` changes the name, the description, or the
  website. An empty `url` removes the website. A new website does not read
  details or images again.
- Products are added only with `read_brand_products`, or by hand in the
  dashboard. Send the `brandId` and a `url`: a store, a collection, a product
  page, or an App Store or Google Play link. It adds up to 20 products, saves
  their photos into the Brand's images, and skips products the Brand already
  has. It takes 5 to 30 seconds. Use it only when the user asks to add products
  from a link, and tell them how many were added (`addedCount`).
- A Brand has no saved colors or fonts. If the user asks to set Brand colors,
  say that a Brand cannot save colors yet. You can still use those colors on
  the slides of a deck.

## Add images

A Brand holds at most 50 images and 60 products. Never pass image bytes as a
tool argument.

- A public image link works directly: pass it to `add_product_images` as
  `{ url }`.
- In an MCP Apps host, call `render_upload` with the `workspace` and ask the
  user to drop the file there. When its message arrives, pass each returned
  `mediaId` to `add_product_images` as `{ mediaId }`. A file attached in chat
  goes the same way, even when the host gives you a url for it.
- With a shell (Claude Code, Cursor, Codex):
  1. `request_product_image_upload` with the `brandId` and the `contentType`
     (JPEG, PNG, or WebP, at most 10 MB). It returns `uploadUrl` and
     `uploadKey`.
  2. PUT the raw bytes to `uploadUrl` with that `Content-Type`.
  3. `add_product_images` with the `brandId` and up to 20
     `{ uploadKey, filename }` entries in one call. To retry, send the same
     list in the same order. Image names are made in the background.
- `rename_product_image` changes an image name. `remove_product_image` deletes
  an image permanently: use it only when the user asks to remove that image.

## Showing results

- In an MCP Apps host, show the Brand with its product images with
  `render_library`.
- Without App tools, tell the user the Brand name and what changed in one or
  two short sentences, and end with its `dashboardUrl` on its own line.
- Do not repeat the website or description unless the user asks. Never
  hand-build a gallery in chat.
