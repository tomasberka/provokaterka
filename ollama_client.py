"""
Ollama API klient pro BaddieOS.
Komunikuje s lokálním Ollama serverem pro generování textu.
Fallback: pokud Ollama neběží, vrátí None – app použije šablony.
"""

import requests
from typing import Optional


class OllamaClient:
    """Klient pro komunikaci s Ollama REST API."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2",
        temperature: float = 0.8,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature

    def is_available(self) -> bool:
        """Zkontroluje dostupnost Ollama serveru."""
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return r.status_code == 200
        except (requests.ConnectionError, requests.Timeout):
            return False

    def get_models(self) -> list[str]:
        """Vrátí seznam dostupných modelů."""
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if r.status_code == 200:
                data = r.json()
                return [m["name"] for m in data.get("models", [])]
        except (requests.ConnectionError, requests.Timeout, ValueError):
            pass
        return []

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 500,
    ) -> Optional[str]:
        """Generuje text. Vrátí None při chybě."""
        try:
            payload = {
                "model": self.model,
                "prompt": user_prompt,
                "system": system_prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": max_tokens,
                },
            }
            r = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60,
            )
            if r.status_code == 200:
                return r.json().get("response", "").strip()
        except (requests.ConnectionError, requests.Timeout, ValueError):
            pass
        return None

    def chat(
        self,
        messages: list[dict],
        system_prompt: str = "",
    ) -> Optional[str]:
        """Chat completion. Vrátí None při chybě."""
        try:
            all_messages = []
            if system_prompt:
                all_messages.append({"role": "system", "content": system_prompt})
            all_messages.extend(messages)
            payload = {
                "model": self.model,
                "messages": all_messages,
                "stream": False,
                "options": {"temperature": self.temperature},
            }
            r = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60,
            )
            if r.status_code == 200:
                return r.json().get("message", {}).get("content", "").strip()
        except (requests.ConnectionError, requests.Timeout, ValueError):
            pass
        return None
