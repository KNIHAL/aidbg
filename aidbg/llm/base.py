# aidbg/llm/base.py
class LLMClient:
    def complete(self, system: str, user: str) -> str:
        raise NotImplementedError
