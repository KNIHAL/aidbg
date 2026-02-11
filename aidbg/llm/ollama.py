# aidbg/llm/ollama.py
from aidbg.llm.base import LLMClient

class OllamaClient(LLMClient):
    def __init__(self, model: str):
        try:
            import requests
        except ImportError:
            raise RuntimeError(
                "Ollama provider selected but requests package is not installed.\n"
                "Install it using: pip install aidbg[ollama]"
            )

        self.requests = requests
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def complete(self, system: str, user: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"{system}\n\n{user}",
            "stream": False,
        }

        try:
            res = self.requests.post(self.url, json=payload, timeout=60)
            res.raise_for_status()
        except self.requests.exceptions.ConnectionError:
            raise RuntimeError(
                "Ollama is not running on http://localhost:11434.\n"
                "Start it using: ollama serve"
            )
        except self.requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama request failed: {e}")

        return res.json()["response"]

