"""
CRM stránka – správa fanoušků s CRUD operacemi, filtrováním a CSV exportem.
"""

import streamlit as st
from datetime import datetime

from config import TIERS, TIER_COLORS, TIER_EMOJI
from database import load_db, save_db, get_df, add_fan, update_fan, delete_fan, export_csv


def page_crm():
    """CRM modul pro správu fanoušků."""
    st.title("👥 CRM & Třídění 'Vojáčků'")
    st.markdown("Správa tvé fanouškovské základny")

    # CSV Export
    csv_data = export_csv()
    if csv_data:
        st.download_button(
            label="📥 Exportovat do CSV",
            data=csv_data,
            file_name=f"fans_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    # Přidání nového fanouška
    with st.expander("➕ Přidat nového fanouška", expanded=False):
        with st.form("add_fan_form"):
            nickname = st.text_input("Nickname *")
            tier = st.selectbox("Tier *", TIERS)
            total_support = st.number_input("Celková podpora (Kč)", min_value=0, value=0)
            notes = st.text_area("Poznámky")
            migrate_telegram = st.checkbox("Migrovat na Telegram?")

            submitted = st.form_submit_button("💾 Přidat")

            if submitted:
                success, message = add_fan(nickname, tier, total_support, notes, migrate_telegram)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    st.markdown("---")

    # Filtry
    st.subheader("🔍 Filtry")
    col1, col2 = st.columns(2)

    with col1:
        tier_filter = st.multiselect("Filtrovat podle tier", TIERS, default=TIERS)

    with col2:
        search = st.text_input("Hledat podle nickname")

    # Načtení a filtrování dat
    df = get_df()

    if not df.empty:
        # Aplikace filtrů
        df_filtered = df[df["tier"].isin(tier_filter)]
        if search:
            df_filtered = df_filtered[df_filtered["nickname"].str.contains(search, case=False, na=False)]

        st.markdown(f"**Zobrazeno:** {len(df_filtered)} / {len(df)} fanoušků")

        # Zobrazení tabulky
        if not df_filtered.empty:
            for idx, row in df_filtered.iterrows():
                emoji = TIER_EMOJI[row["tier"]]

                # VIP řádky zvýrazněné
                if row["tier"] == "VIP":
                    st.markdown(f"""
                    <div class="vip-row">
                        <strong>{emoji} {row['nickname']}</strong> |
                        <em>{row['tier']}</em> |
                        <strong>{int(row['total_support'])} Kč</strong>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"**{emoji} {row['nickname']}** | *{row['tier']}* | **{int(row['total_support'])} Kč**")

                # Expander pro detail/editaci
                with st.expander(f"Detail: {row['nickname']}"):
                    st.markdown(f"**Poznámky:** {row.get('notes', 'Žádné poznámky')}")
                    st.markdown(f"**Telegram:** {'✅ Ano' if row.get('migrate_telegram') else '❌ Ne'}")
                    st.markdown(f"**Vytvořeno:** {row.get('created', 'N/A')}")

                    # Editace fanouška
                    with st.form(f"edit_form_{idx}"):
                        st.markdown("**✏️ Upravit fanouška**")
                        new_tier = st.selectbox(
                            "Tier", TIERS,
                            index=TIERS.index(row["tier"]),
                            key=f"edit_tier_{idx}"
                        )
                        new_support = st.number_input(
                            "Celková podpora (Kč)",
                            min_value=0,
                            value=int(row["total_support"]),
                            key=f"edit_support_{idx}"
                        )
                        new_notes = st.text_area(
                            "Poznámky",
                            value=row.get("notes", ""),
                            key=f"edit_notes_{idx}"
                        )
                        new_telegram = st.checkbox(
                            "Migrovat na Telegram?",
                            value=bool(row.get("migrate_telegram", False)),
                            key=f"edit_telegram_{idx}"
                        )

                        edit_submitted = st.form_submit_button("💾 Uložit změny")
                        if edit_submitted:
                            success, message = update_fan(
                                row["nickname"],
                                tier=new_tier,
                                total_support=new_support,
                                notes=new_notes,
                                migrate_telegram=new_telegram
                            )
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

                    # Tlačítko pro smazání
                    if st.button(f"🗑️ Smazat {row['nickname']}", key=f"delete_{idx}"):
                        success, message = delete_fan(row["nickname"])
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("Žádní fanoušci neodpovídají filtrům.")
    else:
        st.info("Zatím žádní fanoušci v databázi. Přidej prvního pomocí formuláře výše!")
