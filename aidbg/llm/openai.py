# aidbg/llm/openai.py
from aidbg.llm.base import LLMClient

class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str):
        try:
            from openai import OpenAI
        except ImportError:
            raise RuntimeError(
                "OpenAI provider selected but openai package is not installed.\n"
                "Install it using: pip install aidbg[openai]"
            )

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def complete(self, system: str, user: str) -> str:
        res = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return res.choices[0].message.content
