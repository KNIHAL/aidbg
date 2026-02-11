from pathlib import Path
import json
from aidbg.config import load_config

def test_load_global_config(tmp_path, monkeypatch):
    cfg_dir = tmp_path / ".aidbg"
    cfg_dir.mkdir()
    cfg_file = cfg_dir / "config.json"
    cfg_file.write_text(json.dumps({"provider": "groq"}))

    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    cfg = load_config()
    assert cfg["provider"] == "groq"
