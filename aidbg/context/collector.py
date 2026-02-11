# aidbg/context/collector.py
from pathlib import Path

def extract_error_location(traceback: str):
    lines = traceback.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith('File '):
            parts = line.split(',')
            file_path = parts[0].split('"')[1]
            line_no = int(parts[1].strip().replace('line ', ''))
            return file_path, line_no
    return None, None


def get_code_snippet(file_path: str, line_no: int, context: int = 30):
    path = Path(file_path)
    if not path.exists():
        return ""

    code = path.read_text().splitlines()
    start = max(line_no - context - 1, 0)
    end = min(line_no + context, len(code))
    snippet = code[start:end]

    return "\n".join(
        f"{i+start+1}: {line}"
        for i, line in enumerate(snippet)
    )
