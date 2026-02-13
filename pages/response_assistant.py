"""
Response Assistant stránka – generování odpovědí na zprávy fanoušků.
"""

import streamlit as st

from config import RESPONSE_TEMPLATES
from responses import classify_message, generate_response
from ollama_client import OllamaClient


def page_response_assistant():
    """Modul pro generování odpovědí na zprávy."""
    st.title("💬 'Inteligentní Provokatérka'")
    st.markdown("AI asistent pro odpovídání na zprávy fanoušků")

    # Ollama status
    ollama = OllamaClient()
    ollama_available = ollama.is_available()

    if ollama_available:
        st.success("🤖 Ollama je dostupná – odpovědi budou generovány AI!")
    else:
        st.info("💡 Ollama není dostupná – používám šablony. Spusť `ollama serve` pro AI odpovědi.")

    # Nastavení persony
    with st.expander("⚙️ Nastavení Persony", expanded=False):
        persona_name = st.text_input("Jméno persony", value="BaddieBabe")
        persona_lore = st.text_area(
            "Persona Lore (background příběh)",
            value="Jsem sebevědomá, trochu drzá, ale vtipná digitální influencerka. Miluji zábavu a komunikaci s fanoušky.",
            height=100
        )

    st.markdown("---")

    # Input zprávy
    st.subheader("📩 Zpráva od fanouška")
    user_message = st.text_area("Napiš zprávu od fanouška:", height=100, key="user_msg")

    col1, col2 = st.columns(2)
    with col1:
        generate_btn = st.button("🎲 Generovat odpověď", type="primary")
    with col2:
        regenerate_btn = st.button("🔄 Jiná varianta")

    # Generování odpovědi
    if (generate_btn or regenerate_btn) and user_message.strip():
        category, response = generate_response(
            user_message,
            persona_name=persona_name,
            persona_lore=persona_lore,
            ollama_client=ollama if ollama_available else None
        )

        st.markdown("---")
        st.subheader("💬 Vygenerovaná odpověď")

        source_label = "🤖 AI (Ollama)" if ollama_available else "📝 Šablona"
        st.markdown(f"**Kategorie:** `{category.upper()}` | **Zdroj:** {source_label}")

        st.markdown(f"""
        <div class="status-card">
            {response}
        </div>
        """, unsafe_allow_html=True)

        # Kopírovací pole
        st.code(response, language=None)

    elif (generate_btn or regenerate_btn):
        st.warning("⚠️ Napiš nejprve zprávu od fanouška!")

    # Přehled šablon
    with st.expander("📚 Přehled šablon odpovědí"):
        for category, templates in RESPONSE_TEMPLATES.items():
            st.markdown(f"**{category.upper()}**")
            for template in templates:
                st.markdown(f"- {template}")
            st.markdown("")
