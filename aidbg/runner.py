# aidbg/runner.py

import subprocess
import sys
from pathlib import Path
from aidbg.trigger import detect_crash


def run_program(script: str):
    cmd = [sys.executable, script]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    full_output = ""
    if result.stdout:
        full_output += result.stdout + "\n"
    if result.stderr:
        full_output += result.stderr

    if result.returncode != 0:
        project_root = Path(script).resolve().parent
        detect_crash(full_output, project_root)
    else:
        print("✓ Program finished successfully")
