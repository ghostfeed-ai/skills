---
name: ghostfeed-collections
description: Build Ghostfeed image collections. Make a collection, or fill one from a Pinterest search, pin or board, or from the user's own photos.
compatibility: Requires the Ghostfeed MCP server (https://api.ghostfeed.ai/api/v2/mcp) and a Ghostfeed account.
---

> **This skill runs on the Ghostfeed MCP server.** Its tools, models and
> settings are Ghostfeed's, so check first that the Ghostfeed tools (`get_me`,
> `list_skills`, `get_skill`) are available.
>
> - **Connected:** call `get_skill` with `ghostfeed-collections` and follow that copy. The
>   server always has the current version, and it serves the other skills this
>   one loads.
> - **Not connected:** stop and ask the user to connect Ghostfeed at
>   `https://api.ghostfeed.ai/api/v2/mcp`
>   (setup: https://ghostfeed.ai/docs). Do not run these steps with other
>   image, video or music tools.

A collection is a saved folder of images in the workspace; slideshows use it
later. Build one when the user asks to save, collect, or gather images, to
turn a Pinterest pin or board into a collection, or to put their own photos in
one. These are the same steps as Add images in the dashboard's Collections,
and they are free. Avatars are not collections: a person's photos live in
Avatars (`list_avatars`), so never make a collection for an avatar.

## Before you start

Call `list_workspaces` once. If it returns one workspace, use it without
asking. If there are several, ask which one, with the host's own question UI
if it has one. Pass that `workspace` on every write.

## The flow

1. Find or make the collection. When the user names an existing one, find it
   with `list_collections` and `includeEmpty: true` (a new collection has no
   images yet) and match the name loosely. Otherwise `create_collection` with
   the `workspace` and a short `name`: the user's words, or the board's
   `suggestedName`. Do not stop to ask for a name the user did not give. Do
   not make a second collection with the same name; reuse the first.
2. Find the images.
   - From a search: `search_pinterest` with queries for real scenes (a moment
     someone photographed, not topic words). Look at the results and keep only
     images that fit the brief and pass the camera-roll test (no baked-in
     text, logos, or watermarks). Keep the number the user asked for;
     otherwise about 20. In an MCP Apps host you can show the picks with
     `render_library` before you save them.
   - From a Pinterest pin or board link: `import_pinterest_url` with the link.
     It returns a `jobId` at once. Then call `get_pinterest_import` with that
     `jobId` and `waitMs: 25000` until `status` is `succeeded` or `failed`.
     Starting the same link again while it runs returns the same job. If it
     fails because it stopped, you may start it once more. A board gives up to
     100 images and its `suggestedName`. Save all of them unless the user asked
     you to choose.
   - From the user's own photos: never pass image bytes or a url of the file
     as a tool argument. In an MCP Apps host, call `render_upload` with the
     `workspace` and ask the user to drop the photos there; a file attached in
     chat goes the same way. Keep each returned `mediaId`. With a shell
     (Claude Code, Cursor, Codex), for each file call `request_media_upload`,
     PUT the raw bytes to its `uploadUrl` with that `Content-Type`, then call
     `complete_media_upload` with the `uploadId`; it returns the `mediaId`.
3. Save them. `add_collection_images` with the `collectionId`, Pinterest
   urls in `imageUrls` and uploaded photos' `mediaId`s in `mediaIds`, up to 50
   in all per call; send the rest in more calls. A collection holds at most
   100 images, so send no more than 100 minus its `imageCount`. Each image is
   copied into Ghostfeed storage. Images already in the collection
   are skipped. If a call times out, check the collection with
   `list_collection_images` before you send it again. If one image fails,
   nothing in that call is saved and the error names the image: remove it and
   send the call again.
4. Show the result.
   - In an MCP Apps host, show the collection's images with `render_library`.
   - Without App tools, say the collection's name and how many images it now
     holds (`imageCount`), and end with its `dashboardUrl` on its own line.
   - Never hand-build a gallery in chat.
