---
name: apply-action-plan
description: Walk the user through their Stayrank action plan, one fix at a time. Use when the user asks "what's left to do", wants to apply the recommendations, needs the exact text to paste on Airbnb, or says they have done a fix.
---

1. Call `list_actions` (optionally for one listing). Order is by impact: start with the first one.
2. For the current action call `get_action`. Show:
   - what to change and why, in one sentence;
   - the exact text to copy, in a code block when it is a title, description or answer;
   - where to paste it on Airbnb (the path returned by the tool).
3. If the user wants a different wording, adjust it together and save it with `update_action_text`.
4. When the user confirms they applied it, call `complete_action`. If they want to come back later, `snooze_action`; if it does not apply to them, `dismiss_action`. `reopen_action` undoes either.
5. Move to the next action. After several fixes, suggest `refresh_report` to see the updated score.

Never say a change was made on Airbnb: Stayrank cannot edit the listing, the user does.
