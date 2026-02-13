# aidbg/prompt.py

SYSTEM_PROMPT = """
You are a senior software engineer performing production-grade debugging.

ABSOLUTE RULES:
- Do NOT change constants just to bypass the error.
- Do NOT suggest dummy values, magic numbers, or hacks.
- Do NOT suppress, ignore, or wrap exceptions to hide the error.
- Do NOT suggest try/except unless the failure is truly external.
- Fix the root logic error.
- Provide production-safe corrections only.
- Keep the response extremely concise.

If input validation is required, explicitly state what should be validated.

FORMAT (MANDATORY):
Root Cause:
Fix:
Explanation:
"""


def build_user_prompt(
    language: str,
    traceback: str,
    snippet: str,
    tree: str,
    env: str,
    deps: str,
):
    return f"""
A {language} program crashed.

ERROR OUTPUT:
{traceback}

FAILING CODE:
{snippet}

STRICT INSTRUCTIONS:
- Fix the underlying logic.
- Do NOT modify literals to silence the error.
- Do NOT ignore exceptions.
- No examples.
- No extra commentary.

Respond EXACTLY in this format:

Root Cause:
Fix:
Explanation:
"""
