## How Hindsight memory is used

- **What we store:** the team's coding rules, and the team's feedback on each review comment (accepted or rejected, with the date and counts).
- **When we recall:** before every review, the agent looks up memories that match the code.
- **How it learns:** every accept or reject is saved, so the next review changes.
- **Fresh vs trained:** a fresh agent gives generic comments, but the trained agent cites the team's own rules.
- **Where:** `memory.py` (recall and retain) and `seed_memory.py` (loads the starting rules).