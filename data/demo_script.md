# Demo Script: AI Accounts Payable Agent

**Length:** 2 to 3 minutes
**Core message:** The agent gets smarter with every case it remembers.

## Before you start (setup checklist)
- [ ] App is running (command from Person 3)
- [ ] Memory is in the starting state agreed with Person 1 (empty OR preloaded with history cases)
- [ ] `data/rules.json` and `data/invoices.json` are loaded
- [ ] Browser zoom is large enough to read on video

## Opening line (10 seconds)
"Finance teams handle thousands of invoices, and the same mistakes keep coming back.
Our AP agent remembers every past exception and how it was fixed."

## Steps

### Step 1: First-time exception (no memory)
- **Action:** Submit INV-A-101 (Apex Office Supplies, missing PO number).
- **Agent should:** Flag rule R1 (valid PO required) and give a generic suggestion.
- **Audience should notice:** The agent catches the error, but has no vendor history yet.
- **Say:** "This is the first time we've seen this vendor's problem, so the advice is generic."
- (Skip this step if memory is preloaded with history.)

### Step 2: Human resolves it, agent learns
- **Action:** Enter the resolution: "Got PO-5521 from procurement; approved by Team Manager."
- **Agent should:** Save it as a memory