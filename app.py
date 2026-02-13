"""
BaddieOS v2.0 – Command Center pro Digitální Provokatérku
==========================================================
Streamlit dashboard pro správu fanouškovské základny.

Modulární architektura:
- config.py: Konstanty, šablony, nastavení
- database.py: CRUD operace, CSV export
- responses.py: Klasifikace zpráv, generování odpovědí/statusů
- ollama_client.py: Ollama API klient (volitelné AI)
- pages/: Jednotlivé stránky UI
"""

import streamlit as st

from pages.dashboard import page_dashboard
from pages.crm import page_crm
from pages.response_assistant import page_response_assistant
from pages.safety import page_safety_checklist
from pages.status import page_status_generator


# ============================================================================
# SETUP & STYLING
# ============================================================================

def setup_page():
    """Nastaví stránku a custom CSS."""
    st.set_page_config(
        page_title="BaddieOS v2.0",
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
        <style>
        /* VIP řádky v tabulce */
        .vip-row {
            background-color: #ffc10733 !important;
            border-left: 4px solid #ffc107;
            padding: 8px;
            margin: 4px 0;
        }

        /* Safe badge */
        .safe-badge {
            background-color: #28a745;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 18px;
        }

        /* Unsafe badge */
        .unsafe-badge {
            background-color: #dc3545;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 18px;
        }

        /* Status cards */
        .status-card {
            background-color: #262730;
            border: 1px solid #0d6efd;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
        }

        /* Metric cards */
        .metric-card {
            background-color: #262730;
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)


# ============================================================================
# SIDEBAR NAVIGACE
# ============================================================================

def sidebar() -> str:
    """Zobrazí sidebar s navigací."""
    with st.sidebar:
        st.markdown("# 🎭 BaddieOS")
        st.markdown("**Command Center v2.0**")
        st.markdown("---")

        page = st.radio(
            "Navigace",
            [
                "📊 Dashboard",
                "👥 CRM & Vojáčci",
                "💬 Response Assistant",
                "🔒 Safety Checklist",
                "📡 Status Generator"
            ]
        )

        st.markdown("---")
        st.markdown("**Verze:** 2.0.0")
        st.markdown("**Status:** 🟢 Online")

        return page


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Hlavní vstupní bod aplikace."""
    setup_page()
    page = sidebar()

    # Routing
    if page == "📊 Dashboard":
        page_dashboard()
    elif page == "👥 CRM & Vojáčci":
        page_crm()
    elif page == "💬 Response Assistant":
        page_response_assistant()
    elif page == "🔒 Safety Checklist":
        page_safety_checklist()
    elif page == "📡 Status Generator":
        page_status_generator()


if __name__ == "__main__":
    main()
