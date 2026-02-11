from pathlib import Path

def get_project_tree(root: Path, max_depth: int = 2) -> str:
    lines = []

    def walk(path: Path, depth: int):
        if depth > max_depth:
            return
        for p in sorted(path.iterdir()):
            if p.name.startswith("."):
                continue
            lines.append("  " * depth + p.name + ("/" if p.is_dir() else ""))
            if p.is_dir():
                walk(p, depth + 1)

    walk(root, 0)
    return "\n".join(lines)
