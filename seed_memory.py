import json
from memory import client

TEAM = "demo-team"

try:
    client.create_bank(bank_id=TEAM, name="Demo Team")
except Exception as e:
    print("Bank note:", e)

with open("data/rules.json", encoding="utf-8") as f:
    rules = json.load(f)

for r in rules:
    client.retain(
        bank_id=TEAM,
        content=f"Team rule {r['id']} ({r['name']}): {r['rule']}",
        context="team coding standard",
    )

print("Seeded", len(rules), "rules into", TEAM)
client.close()