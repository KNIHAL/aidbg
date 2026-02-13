# aidbg/languages/python.py
import re
from pathlib import Path
from aidbg.languages.base import LanguageAdapter


class PythonAdapter(LanguageAdapter):
    def detect_crash(self, output: str) -> bool:
        return "Traceback (most recent call last)" in output

    def extract_location(self, output: str) -> tuple[str | None, int | None]:
        pattern = r'File "(.+?)", line (\d+)'
        matches = re.findall(pattern, output)

        if not matches:
            return None, None

        file_path, line_no = matches[-1]
        return file_path, int(line_no)

    def get_snippet(self, file_path: str, line_no: int, context: int = 3) -> str:
        try:
            path = Path(file_path)
            lines = path.read_text().splitlines()

            start = max(line_no - context - 1, 0)
            end = min(line_no + context, len(lines))

            snippet = []
            for i in range(start, end):
                snippet.append(f"{i+1}: {lines[i]}")

            return "\n".join(snippet)
        except Exception:
            return ""

    def classify_error(self, output: str) -> str:
        simple_errors = [
            "ZeroDivisionError",
            "NameError",
            "TypeError",
            "ImportError",
            "ModuleNotFoundError",
            "AttributeError",
        ]

        for err in simple_errors:
            if err in output:
                return "simple"

        return "complex"
