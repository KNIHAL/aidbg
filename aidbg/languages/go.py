import re
from pathlib import Path
from aidbg.languages.base import LanguageAdapter


class GoAdapter(LanguageAdapter):
    def detect_crash(self, output: str) -> bool:
        # Go runtime panic or compile error
        return (
            "panic:" in output
            or "fatal error:" in output
            or "invalid operation:" in output
        )

    def extract_location(self, output: str) -> tuple[str | None, int | None]:
        """
        Matches patterns like:
        examples/test.go:7:21: invalid operation: division by zero
        or
        /path/to/file.go:12 +0x39
        """
        pattern = r'(.+?\.go):(\d+)'
        match = re.search(pattern, output)

        if not match:
            return None, None

        file_path = match.group(1)
        line_no = int(match.group(2))
        return file_path, line_no

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
        simple_patterns = [
            "division by zero",
            "undefined:",
            "cannot use",
            "invalid operation",
        ]

        for pattern in simple_patterns:
            if pattern in output:
                return "simple"

        return "complex"
