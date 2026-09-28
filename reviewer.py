import json, os, re, time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ["GROQ_API_KEY"])

MODELS = ["openai/gpt-oss-120b", "qwen/qwen3-32b"]   # primary, fallback
PROMPTS = Path(__file__).parent / "prompts"

def _load(name: str) -> str:
    return (PROMPTS / name).read_text(encoding="utf-8")

def _format_memories(memories):
    if not memories:
        return "(none)"
    return "\n".join(f"- [{m.get('type','memory')}] {m['text']}" for m in memories)

def _parse_json(text: str) -> dict:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)  # qwen may emit this
    text = re.sub(r"```json|```", "", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object found")
    return json.loads(text[start:end + 1])

def _validate(data: dict) -> dict:
    comments = data.get("comments")
    if not isinstance(comments, list):
        raise ValueError("missing comments list")
    clean = []
    for i, c in enumerate(comments, 1):
        clean.append({
            "id": c.get("id") or f"c{i}",
            "line": c.get("line"),
            "severity": c.get("severity", "info"),
            "suggestion": c.get("suggestion", ""),
            "reason": c.get("reason", ""),
            "memory_ref": c.get("memory_ref"),
        })
    return {"comments": clean}

def review_code(code: str, pr_title: str = "", memories: list[dict] | None = None) -> dict:
    template = _load("review_with_memory.txt" if memories else "review_plain.txt")
    prompt = (template.replace("{code}", code)
                      .replace("{pr_title}", pr_title or "(none)")
                      .replace("{memories}", _format_memories(memories)))

    last_err = None
    for model in MODELS:
        for attempt in range(2):
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    response_format={"type": "json_object"},
                )
                return _validate(_parse_json(resp.choices[0].message.content))
            except Exception as e:
                last_err = e
                time.sleep(1 + attempt)
    return {"comments": [], "error": f"Review failed: {last_err}"}
if __name__ == "__main__":
    code = 'def get_user(id):\n    try:\n        return db.find(id)\n    except:\n        pass'
    fake_memories = [
        {"type": "rule", "text": "All DB calls must catch specific exceptions and log them, never bare except."},
        {"type": "feedback", "text": "Rejected: suggestion to rename 'id' to 'user_id' (team allows short names)."},
    ]
    print("PLAIN:", json.dumps(review_code(code), indent=2))
    print("MEMORY:", json.dumps(review_code(code, memories=fake_memories), indent=2))