import re
from pathlib import Path
from aidbg.languages.base import LanguageAdapter


class JavaAdapter(LanguageAdapter):
    def detect_crash(self, output: str) -> bool:
        # Java stack traces usually contain "Exception in thread"
        return "Exception in thread" in output

    def extract_location(self, output: str):
        # Example:
        # at com.example.Main.main(Main.java:7)
        pattern = r'\((.+\.java):(\d+)\)'
        match = re.search(pattern, output)

        if not match:
            return None, None

        file_path, line_no = match.groups()
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
            "NullPointerException",
            "ArithmeticException",
            "ArrayIndexOutOfBoundsException",
            "IllegalArgumentException",
        ]

        for err in simple_errors:
            if err in output:
                return "simple"

        return "complex"
