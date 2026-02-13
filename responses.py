"""
Generování odpovědí a statusů pro BaddieOS.
Obsahuje keyword klasifikaci a šablonové odpovědi s Ollama fallbackem.
"""

import random
from datetime import datetime
from typing import Optional

from config import KEYWORD_MAP, RESPONSE_TEMPLATES, STATUS_TEMPLATES
from ollama_client import OllamaClient


def classify_message(msg: str) -> str:
    """Klasifikuje zprávu podle klíčových slov."""
    msg_lower = msg.lower()
    for category, keywords in KEYWORD_MAP.items():
        if any(keyword in msg_lower for keyword in keywords):
            return category
    return "fallback"


def generate_response(msg: str, persona_name: str = "BaddieBabe",
                      persona_lore: str = "",
                      ollama_client: Optional[OllamaClient] = None) -> tuple[str, str]:
    """
    Generuje odpověď na zprávu.
    Pokud je Ollama dostupná, použije AI; jinak vrátí šablonu.
    """
    category = classify_message(msg)

    # Pokus o AI generování přes Ollama
    if ollama_client and ollama_client.is_available():
        system_prompt = (
            f"Jsi {persona_name}. {persona_lore} "
            f"Odpovídej krátce, v češtině, s emojis. "
            f"Kategorie zprávy: {category}."
        )
        ai_response = ollama_client.generate(
            system_prompt=system_prompt,
            user_prompt=msg,
            max_tokens=200
        )
        if ai_response:
            return category, ai_response

    # Fallback na šablony
    template = random.choice(RESPONSE_TEMPLATES[category])
    return category, template


def get_auto_period() -> str:
    """Automaticky určí denní období podle aktuálního času."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "ráno"
    elif 12 <= hour < 18:
        return "odpoledne"
    elif 18 <= hour < 23:
        return "večer"
    else:
        return "náhodný"


def generate_status(period: str = "auto",
                    ollama_client: Optional[OllamaClient] = None,
                    persona_name: str = "BaddieBabe") -> str:
    """
    Vygeneruje status pro zvolené období.
    Pokud je Ollama dostupná, použije AI; jinak vrátí šablonu.
    """
    if period == "auto":
        period = get_auto_period()

    # Pokus o AI generování přes Ollama
    if ollama_client and ollama_client.is_available():
        system_prompt = (
            f"Jsi {persona_name}, digitální influencerka. "
            f"Vygeneruj krátký status pro sociální síť. "
            f"Období dne: {period}. Piš česky, s emojis, max 2 věty."
        )
        ai_response = ollama_client.generate(
            system_prompt=system_prompt,
            user_prompt=f"Vygeneruj status pro období: {period}",
            max_tokens=150
        )
        if ai_response:
            return ai_response

    # Fallback na šablony
    templates = STATUS_TEMPLATES.get(period, STATUS_TEMPLATES["náhodný"])
    return random.choice(templates)
