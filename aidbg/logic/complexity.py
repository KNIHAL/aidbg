# aidbg/logic/complexity.py

SIMPLE_ERRORS = (
    "ModuleNotFoundError",
    "ImportError",
    "SyntaxError",
    "IndentationError",
    "NameError",
    "TypeError",
    "AttributeError",
    "ZeroDivisionError",
)

def classify_error(traceback: str) -> str:
    for err in SIMPLE_ERRORS:
        if err in traceback:
            return "simple"
    return "complex"
