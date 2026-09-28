import subprocess, tempfile, os

def run_linter(code: str) -> list[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        out = subprocess.run(["python", "-m", "flake8", path],
                             capture_output=True, text=True, timeout=15)
        return [line.split(":", 1)[-1].strip() for line in out.stdout.splitlines()]
    except Exception as e:
        return [f"linter unavailable: {e}"]
    finally:
        os.unlink(path)
if __name__ == "__main__":
    sample = 'def get_user(id):\n    return db.find(id)\n'
    print(run_linter(sample))