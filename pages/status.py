"""
Status Generator stránka – generování statusů pro sociální sítě.
"""

import streamlit as st
from datetime import datetime

from responses import get_auto_period, generate_status
from ollama_client import OllamaClient


def page_status_generator():
    """Modul pro generování statusů."""
    st.title("📡 'Teď a Tady' – Status Generator")
    st.markdown("Automatické generování statusů pro sociální sítě")

    # Ollama status
    ollama = OllamaClient()
    ollama_available = ollama.is_available()

    if ollama_available:
        st.success("🤖 Ollama je dostupná – statusy budou generovány AI!")

    # Info o aktuálním období
    current_period = get_auto_period()
    hour = datetime.now().hour
    st.info(f"🕐 Aktuální čas: {hour}:00 → Detekované období: **{current_period.upper()}**")

    st.markdown("---")

    # Výběr období
    st.subheader("⚙️ Nastavení")
    period = st.selectbox(
        "Vyber období",
        ["auto", "ráno", "odpoledne", "večer", "náhodný"],
        index=0
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎲 Generovat 1 status", type="primary"):
            status = generate_status(
                period,
                ollama_client=ollama if ollama_available else None
            )
            st.session_state["single_status"] = status

    with col2:
        if st.button("🔄 Generovat 5 statusů"):
            statuses = [
                generate_status(
                    period,
                    ollama_client=ollama if ollama_available else None
                )
                for _ in range(5)
            ]
            st.session_state["batch_statuses"] = statuses

    # Zobrazení jednotlivého statusu
    if "single_status" in st.session_state:
        st.markdown("---")
        st.subheader("💬 Vygenerovaný status")
        st.markdown(f"""
        <div class="status-card">
            {st.session_state['single_status']}
        </div>
        """, unsafe_allow_html=True)
        st.code(st.session_state["single_status"], language=None)

    # Zobrazení dávky statusů
    if "batch_statuses" in st.session_state:
        st.markdown("---")
        st.subheader("📝 Dávka statusů")
        for i, status in enumerate(st.session_state["batch_statuses"], 1):
            st.markdown(f"**Status {i}:**")
            st.markdown(f"""
            <div class="status-card">
                {status}
            </div>
            """, unsafe_allow_html=True)
            st.code(status, language=None)

    st.markdown("---")
    if not ollama_available:
        st.info("💡 Spusť `ollama serve` pro AI generování statusů na míru persony.")
