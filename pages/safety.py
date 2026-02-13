"""
Safety Checklist stránka – kontrola bezpečnosti nahrávaného obsahu.
"""

import streamlit as st


def page_safety_checklist():
    """Modul pro kontrolu bezpečnosti nahrávaného obsahu."""
    st.title("🔒 Content Manager & Bezpečnost")
    st.markdown("5-bodový checklist před uploadem obsahu")

    # File uploader
    uploaded_file = st.file_uploader(
        "📤 Nahraj soubor (foto/video) pro kontrolu",
        type=["jpg", "jpeg", "png", "gif", "mp4", "mov"]
    )

    if uploaded_file:
        # Náhled (pouze pro obrázky)
        if uploaded_file.type.startswith("image/"):
            st.image(uploaded_file, caption="Náhled", use_container_width=True)
        else:
            st.info(f"📹 Video: {uploaded_file.name}")

        st.markdown("---")
        st.subheader("✅ Bezpečnostní checklist")

        # Checklist
        check1 = st.checkbox(
            "✅ Metadata odstraněna (EXIF, GPS, datum)",
            help="Zkontroluj, že soubor nemá EXIF data s polohou nebo časem."
        )
        check2 = st.checkbox(
            "✅ Pozadí je neutrální / nelze identifikovat lokaci",
            help="Žádné charakteristické prvky (ulice, budovy, značky)."
        )
        check3 = st.checkbox(
            "✅ Žádné identifikační znaky (tetování, znaménka, šperky)",
            help="Nic, co by mohlo prozradit identitu."
        )
        check4 = st.checkbox(
            "✅ Face swap aplikován a vypadá přirozeně",
            help="Obličej je vyměněný a není to poznatelné."
        )
        check5 = st.checkbox(
            "✅ Tón pleti a světlo konzistentní s předchozím obsahem",
            help="Barva kůže a osvětlení odpovídá ostatním fotkám/videím."
        )

        # Hodnocení
        total_checks = sum([check1, check2, check3, check4, check5])

        st.markdown("---")
        st.subheader("🎯 Výsledek")

        if total_checks == 5:
            st.markdown("""
            <div class="safe-badge">
                ✅ SAFE TO UPLOAD
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown(f"""
            <div class="unsafe-badge">
                ⚠️ UNSAFE – {total_checks}/5 bodů
            </div>
            """, unsafe_allow_html=True)
            st.warning(f"⚠️ Dokončeno pouze {total_checks}/5 bodů. Nahraj až po splnění všech!")
    else:
        st.info("👆 Nahraj soubor pro zahájení kontroly.")
