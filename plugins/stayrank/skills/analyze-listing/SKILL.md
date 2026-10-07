---
name: analyze-listing
description: Analyze an Airbnb listing with Stayrank and present the result. Use when the user shares an Airbnb listing URL, asks "how good is my listing", "why am I not getting bookings", "what should I fix first", or wants a score, a verdict or a rewritten title or description.
---

1. Resolve the listing. If the user gave an Airbnb URL and it is not in the account yet, call `add_listing` with it (this is free and returns a preview). Otherwise call `list_listings` or pass a piece of the title to the tools.
2. If a full report already exists, call `get_listing_report` and go to step 4.
3. Otherwise call `quote_analysis`. Tell the user what it will use (one listing from their balance) and wait for an explicit yes. Then call `start_analysis` with the returned quote token, and `get_analysis_status` until the status is completed (the analysis takes about two minutes).
4. Present the report in this order, briefly:
   - the score out of 100 and the one-sentence verdict;
   - the listing's strengths (what to keep and put forward);
   - the three highest-impact fixes, each with the ready-to-paste text when there is one;
   - booking settings worth checking, with the trade-off Airbnb mentions;
   - how the listing compares with its neighbors, only when the panel is reliable.
5. Offer the next step: work through the action plan, or improve the photos.

Stay factual. Never promise more bookings or a ranking position, and never claim to know Airbnb's secret algorithm: quote what Airbnb itself says, as the report does.
