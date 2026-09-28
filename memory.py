import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
import json
from datetime import date

load_dotenv()

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.environ["HINDSIGHT_API_KEY"],
)


def recall_context(team_id: str, code: str) -> list[str]:
    """Return past memories that are relevant to this code."""
    result = client.recall(
        bank_id=team_id,
        query=f"Team rules and past review feedback relevant to this code:\n{code}",
    )
    return [m.text for m in result.results]


STATS_FILE = "feedback_stats.json"


def _load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def retain_feedback(team_id: str, comment: str, verdict: str, note: str = ""):
    """Save the team's verdict, with today's date and running accept/reject counts."""
    stats = _load_stats()
    key = f"{team_id}|{comment.strip().lower()}"
    entry = stats.get(key, {"accepted": 0, "rejected": 0})
    if verdict == "accepted":
        entry["accepted"] += 1
    elif verdict == "rejected":
        entry["rejected"] += 1
    stats[key] = entry
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    client.retain(
        bank_id=team_id,
        content=(
            f"[{date.today().isoformat()}] Review comment: {comment}. "
            f"Team verdict: {verdict}. Totals so far for this comment: "
            f"accepted {entry['accepted']} times, rejected {entry['rejected']} times. {note}"
        ),
        context="code review feedback",
    )