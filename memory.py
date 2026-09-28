import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

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


def retain_feedback(team_id: str, comment: str, verdict: str, note: str = ""):
    """Save what the team decided about a review comment."""
    client.retain(
        bank_id=team_id,
        content=f"Review comment: {comment}. Team verdict: {verdict}. {note}",
        context="code review feedback",
    )