---
name: get-started
description: Explain what Stayrank can do and pick the right workflow. Use when the user asks what this plugin does, wants to begin, or is unsure whether to check a listing already in their account, analyze a new Airbnb listing, work through their action plan or improve their photos.
---

Stayrank scores Airbnb listings out of 100 on seven axes (photos, title, description, amenities, reviews, price, trust), ranks the fixes by impact, rewrites the texts, checks the booking settings Airbnb says influence search, compares the listing with the neighbors that rank in the same search, and retouches photos.

Everything except signing up and paying happens here, through the Stayrank tools:

1. Call `get_account` first: it says which organization is connected and how many listings and photo retouches are left.
2. Pick the workflow with the user:
   - **A listing already in the account**: `list_listings`, then `get_listing_report` (score, axes, strengths, settings, competitors, photo coverage).
   - **A new Airbnb listing**: `add_listing` with the Airbnb URL (free preview), then `quote_analysis`, show the quote, and only after the user explicitly agrees call `start_analysis` with the quote token. Poll `get_analysis_status` until it is done.
   - **The action plan**: `list_actions`, `get_action` for the exact text to copy and where to paste it on Airbnb, then `complete_action` once the user has applied it.
   - **Photos**: `plan_photo_enhancement`, then `enhance_listing_photos` (batch) or `enhance_photo` (one photo, a preset or the user's own style).
   - **Competitors**: `compare_with_competitors`.
3. Stayrank never edits the Airbnb listing itself: the user applies each change on Airbnb, Stayrank tracks it.
4. If no listing or retouch is left, say so plainly and give the billing page link returned by the tool. Never invent a price or a purchase.
