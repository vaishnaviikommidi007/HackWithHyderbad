# Code Review Agent That Learns (Hindsight)

An AI code reviewer that remembers your team's coding rules and past review
feedback, so it gives better reviews over time.

## The problem
Generic AI reviewers forget everything. They repeat the same suggestions and
don't know your team's standards.

## What it does
1. You paste code from a pull request.
2. The agent recalls the team's rules and past feedback from Hindsight.
3. It reviews the code using those memories.
4. You mark each comment accepted or rejected, and that feedback is saved.
5. The next review is better.

## Tech stack
- Python
- Hindsight (memory)
- Groq (LLM)
- Streamlit (interface)

## How to run
1. Clone the repo.
2. `pip install -r requirements.txt`
3. Create a `.env` file with your `HINDSIGHT_API_KEY` and Groq key. Never push it.
4. `python seed_memory.py` (loads the team rules once)
5. `streamlit run app.py`

## Project files
- `memory.py`: saving and recalling memories
- `seed_memory.py`: loads the starting team rules
- `reviewer.py`: the AI review logic
- `app.py`: the screen
- `data/`: rules, sample pull requests, demo script

## Team
Add your four names here.
## How Hindsight memory is used

- **What we store:** the team's coding rules, and the team's feedback on each review comment (accepted or rejected, with the date and counts).
- **When we recall:** before every review, the agent looks up memories that match the code.
- **How it learns:** every accept or reject is saved, so the next review changes.
- **Fresh vs trained:** a fresh agent gives generic comments, but the trained agent cites the team's own rules.
- **Where:** `memory.py` (recall and retain) and `seed_memory.py` (loads the starting rules).