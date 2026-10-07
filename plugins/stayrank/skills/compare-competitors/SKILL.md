---
name: compare-competitors
description: Compare an Airbnb listing with the listings that rank around it. Use when the user asks how their listing stacks up, what neighbors offer that they do not, whether their price, rating or photo count is in line, or why others rank higher.
---

1. Call `compare_with_competitors` for the listing. It reads the panel collected during the full analysis: listings from the same Airbnb search for the same stay, in Airbnb's own order.
2. If the panel is unavailable or too small, say so and stop: do not guess. A full analysis (`quote_analysis`, then `start_analysis`) collects it.
3. Otherwise summarize:
   - where the listing sits on price, rating, number of reviews and number of photos against the median;
   - the amenities most of the top listings offer that this one does not list (only ones the host may actually have: suggest checking, never adding something that does not exist);
   - what the listing does better than most.
4. Turn the gaps into actions with the user and point to the matching items of the action plan (`list_actions`).

Never name a competitor negatively and never present the comparison as a ranking guarantee.
