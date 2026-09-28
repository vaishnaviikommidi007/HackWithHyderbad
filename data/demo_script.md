# Demo Script: Code Review Agent with Memory

**Story:** A fresh AI reviewer gives generic comments. Our reviewer remembers
the team's rules and feedback, so it gets better with every review.

## Before the demo
- Bank `demo-fresh` is empty (the fresh agent).
- Bank `demo-team` is seeded with 6 team rules (the trained agent).
- Snippets are in `data/snippets.json`.

## Steps
1. **Fresh agent.** Paste PR-101 (SQL built with an f-string) into the fresh
   agent. Point out: the comments are generic and don't mention any team rule.
2. **Trained agent.** Paste the same PR-101 into the trained agent. Point out:
   it cites the team rule "SQL queries must be parameterized."
3. **Give feedback.** Click "accepted" on the SQL comment. Click "rejected" on
   any generic comment (like a naming suggestion). Point out: the "Memories
   used" panel shows what the agent remembered.
4. **Review again.** Paste PR-102 (another SQL mistake). Point out: the agent now
   also recalls the feedback the team just gave, with the date and counts.
5. **New mistake type.** Paste PR-103 (uses print for logging). Point out: it
   cites the logger rule.
6. **Two problems at once.** Paste PR-105 (hard-coded API key and a bare except).
   Point out: it cites both the secrets rule and the exceptions rule.
7. **Closing line.** "Same code, two agents. The one with memory knows our
   team. That's Hindsight."

## Things to mention
- Feedback is saved with the date and accepted/rejected counts.
- Nothing is hard-coded. The agent's behavior changes only because of memory.