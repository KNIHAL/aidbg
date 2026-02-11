# aidbg/logic/token_budget.py

def get_token_budget(level: str) -> int:
    if level == "simple":
        return 80     # 1–2 lines max
    return 180        # still capped, no essay
