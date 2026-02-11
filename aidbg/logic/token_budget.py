# aidbg/logic/token_budget.py

def get_token_budget(level: str) -> int:
    if level == "simple":
        return 80
    return 180
