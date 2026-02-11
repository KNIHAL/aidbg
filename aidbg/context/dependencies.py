from pathlib import Path

def get_dependencies(root: Path) -> str:
    req = root / "requirements.txt"
    if not req.exists():
        return ""
    lines = []
    for line in req.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            lines.append(line)
    return "\n".join(lines[:20])  # lightweight cap
