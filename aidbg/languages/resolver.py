from pathlib import Path

from aidbg.languages.python import PythonAdapter
from aidbg.languages.javascript import JavaScriptAdapter
from aidbg.languages.go import GoAdapter
from aidbg.languages.java import JavaAdapter


def resolve_adapter(script_path: str):
    ext = Path(script_path).suffix.lower()

    if ext == ".py":
        return PythonAdapter()

    if ext == ".js":
        return JavaScriptAdapter()

    if ext == ".go":
        return GoAdapter()

    if ext == ".java":
        return JavaAdapter()

    raise RuntimeError(f"Unsupported language: {ext}")
