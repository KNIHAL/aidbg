from aidbg.llm.base import LLMClient

class GroqClient(LLMClient):
    def __init__(self, api_key, model):
        try:
            from groq import Groq
        except ImportError:
            raise RuntimeError(
                "Groq provider selected but 'groq' package is not installed.\n"
                "Install it using: pip install aidbg[groq]"
            )

        self.client = Groq(api_key=api_key)
        self.model = model

    def complete(self, system, user):
        res = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return res.choices[0].message.content
