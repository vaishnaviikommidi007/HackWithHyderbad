import re
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
import json
from datetime import date

load_dotenv()

STATS_FILE = "feedback_stats.json"


def get_hindsight_client():
    return Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=os.environ["HINDSIGHT_API_KEY"],
    )


def recall_context(team_id: str, code: str) -> list[dict]:
    """Return past memories relevant to this code."""
    client = get_hindsight_client()

    result = client.recall(
        bank_id=team_id,
        query=f"Team rules and past review feedback relevant to this code:\n{code}",
    )

    memories = []

    for m in result.results:
        text = m.text

        counts = re.search(
            r"Totals so far for this comment:\s*accepted\s+(\d+)\s+times,\s*rejected\s+(\d+)\s+times",
            text,
            re.IGNORECASE
        )

        memory = {
            "type": m.type,
            "text": text,
            "date": str(m.occurred_start) if m.occurred_start else None,
            "metadata": m.metadata or {},
            "accepted": int(counts.group(1)) if counts else None,
            "rejected": int(counts.group(2)) if counts else None,
        }

        memories.append(memory)

    return memories

def _load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def retain_feedback(team_id: str, comment: str, verdict: str, note: str = ""):
    """Save the team's verdict with running accept/reject counts."""
    stats = _load_stats()

    key = f"{team_id}|{comment.strip().lower()}"

    entry = stats.get(
        key,
        {
            "accepted": 0,
            "rejected": 0
        }
    )

    if verdict == "accepted":
        entry["accepted"] += 1

    elif verdict == "rejected":
        entry["rejected"] += 1

    stats[key] = entry

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    get_hindsight_client().retain(
        bank_id=team_id,
        content=(
            f"[{date.today().isoformat()}] "
            f"Review comment: {comment}. "
            f"Team verdict: {verdict}. "
            f"Totals so far for this comment: "
            f"accepted {entry['accepted']} times, "
            f"rejected {entry['rejected']} times. "
            f"{note}"
        ),
        context="code review feedback",
    )