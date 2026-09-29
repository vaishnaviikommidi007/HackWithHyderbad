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
    lines = []
    for i, m in enumerate(memories, 1):
        meta = [m.get("type", "memory")]
        if m.get("date"):
            meta.append(f"date {m['date']}")
        if m.get("accepted") is not None:
            meta.append(f"accepted {m['accepted']}")
        if m.get("rejected") is not None:
            meta.append(f"rejected {m['rejected']}")
        lines.append(f"[M{i}] ({', '.join(meta)}) {m['text']}")
    return "\n".join(lines)

def _parse_json(text: str) -> dict:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)  # qwen may emit this
    text = re.sub(r"```json|```", "", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object found")
    return json.loads(text[start:end + 1])

def _validate(data: dict, memories=None) -> dict:
    comments = data.get("comments")
    if not isinstance(comments, list):
        raise ValueError("missing comments list")
    by_id = {f"M{i}": m for i, m in enumerate(memories or [], 1)}
    clean = []
    for i, c in enumerate(comments, 1):
        mem = by_id.get(c.get("memory_id"))   # unknown or null IDs become None
        evidence = None
        if mem and mem.get("accepted") is not None:
            evidence = f"Accepted {mem['accepted']}, rejected {mem.get('rejected', 0)}"
        clean.append({
            "id": c.get("id") or f"c{i}",
            "line": c.get("line"),
            "severity": c.get("severity", "info"),
            "suggestion": c.get("suggestion", ""),
            "reason": c.get("reason", ""),
            "memory_ref": mem["text"] if mem else None,
            "evidence": evidence,
            "rule_update": c.get("rule_update") if mem else None,
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
                return _validate(_parse_json(resp.choices[0].message.content), memories)
            except Exception as e:
                last_err = e
                time.sleep(1 + attempt)
    return {"comments": [], "error": f"Review failed: {last_err}"}
if _name_ == "_main_":
    code = 'var total = 0;\ntry {\n  total = compute();\n} catch (e) {}'
    memories = [
        {"type": "rule", "date": "2026-08-01", "accepted": 3, "rejected": 0,
         "text": "Use var for variables in this codebase."},
        {"type": "rule", "date": "2026-09-20", "accepted": 4, "rejected": 0,
         "text": "Use const or let, never var."},
        {"type": "rule", "date": "2026-08-10", "accepted": 5, "rejected": 1,
         "text": "Never leave an empty catch block; log the error."},
    ]
    print("PLAIN:", json.dumps(review_code(code), indent=2))
    print("MEMORY:", json.dumps(review_code(code, memories=memories), indent=2))