
import json
from pathlib import Path
from typing import Optional

def load_config(project_root: Optional[Path] = None):
    paths = []

    if project_root:
        paths.append(project_root / ".aidbg" / "config.json")

    paths.append(Path.home() / ".aidbg" / "config.json")

    for p in paths:
        if p.exists():
            return json.loads(p.read_text())

    raise RuntimeError("No config found. Run `aidbg init` or create a config.")
