---
name: improve-photos
description: Improve the photos of an Airbnb listing with the Stayrank photo studio. Use when the user wants brighter, straighter or cleaner photos, asks which photos need work, wants to retouch the whole listing at once, wants a specific look ("warm evening light", "more natural colors"), or wants to see a room redecorated.
---

1. Call `plan_photo_enhancement` for the listing. It says which photos need work, the preset chosen for each, how many retouches it will use and how many are left. Show that plan and wait for a yes.
2. For the whole listing call `enhance_listing_photos`. It processes as many photos as fit in one call and returns what is done and what remains: call it again until nothing remains (it skips photos already done, so repeating is safe). `get_photo_job` shows progress.
3. For one photo call `enhance_photo` with a preset (auto, brighten, straighten, declutter, sky, hdr, twilight) or with `custom` and the user's own style in a short sentence.
4. Redecoration (`decorate_photo`) is a separate, clearly labeled preview of furniture and decor; it is not a retouch of the real room.
5. `list_photo_edits` returns the before/after pairs and download links.

Retouches never change the room itself: nothing is added or removed. Say so if the user asks for something that would misrepresent the property (adding a pool, removing a building, enlarging a room) and offer what the studio can honestly do instead.
