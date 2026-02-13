import subprocess
import sys
from pathlib import Path

from aidbg.trigger import handle_crash
from aidbg.languages.resolver import resolve_adapter


def run_program(script: str):
    ext = Path(script).suffix.lower()

    try:
        # ---------- COMMAND RESOLUTION ----------
        if ext == ".py":
            cmd = [sys.executable, script]

        elif ext == ".js":
            cmd = ["node", script]

        elif ext == ".go":
            cmd = ["go", "run", script]

        elif ext == ".java":
            # Compile first
            compile_result = subprocess.run(
                ["javac", script],
                capture_output=True,
                text=True,
            )

            if compile_result.returncode != 0:
                adapter = resolve_adapter(script)
                project_root = Path(script).resolve().parent
                handle_crash(
                    compile_result.stderr,
                    project_root,
                    adapter,
                )
                return

            class_name = Path(script).stem
            cmd = ["java", "-cp", str(Path(script).parent), class_name]

        else:
            raise RuntimeError(f"Unsupported language: {ext}")

        # ---------- EXECUTION ----------
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

    except FileNotFoundError as e:
        print(f"Runtime not found for {ext} files.")
        print(str(e))
        return

    # ---------- OUTPUT MERGE ----------
    full_output = ""
    if result.stdout:
        full_output += result.stdout + "\n"
    if result.stderr:
        full_output += result.stderr

    # ---------- CRASH HANDLING ----------
    if result.returncode != 0:
        adapter = resolve_adapter(script)
        project_root = Path(script).resolve().parent
        handle_crash(full_output, project_root, adapter)
    else:
        print("✓ Program finished successfully")
