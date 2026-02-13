"""
BaddieOS v1.0 – Command Center pro Digitální Provokatérku
==========================================================
Streamlit dashboard pro správu fanouškovské základny.
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from typing import Optional
import random

# Import Ollama klienta (připraveno na budoucí integraci)
from ollama_client import OllamaClient


DB_FILE = "fans_db.json"
DB_COLUMNS = ["nickname", "tier", "total_support", "notes", "migrate_telegram", "created"]


def load_db() -> list:
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_db(data: list) -> None:
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_df() -> pd.DataFrame:
    data = load_db()
    if not data:
        return pd.DataFrame(columns=DB_COLUMNS)
    return pd.DataFrame(data)


TIERS = ["Free", "Supporter", "VIP"]
TIER_COLORS = {
    "Free": "#6c757d",
    "Supporter": "#0d6efd",
    "VIP": "#ffc107"
}
TIER_EMOJI = {
    "Free": "👤",
    "Supporter": "⭐",
    "VIP": "👑"
}


# Response Assistant templates
KEYWORD_MAP = {
    "pozdrav": ["ahoj", "nazdar", "čau", "zdravím", "dobrý", "hej", "halo"],
    "kompliment": ["krásná", "nádherná", "sexy", "parádní", "úžasná", "bomba", "kráska", "líbíš"],
    "obsah": ["foto", "fotka", "video", "obsah", "příspěvek", "nový", "kdy", "ukáž"],
    "sraz": ["sraz", "meeting", "osobně", "potkat", "vidět", "sejít", "sejdeme"],
    "vulgární": ["sex", "prd", "kunda", "pica", "péro", "šukat", "píča"],
    "dárek": ["dárek", "gift", "poslat", "support", "podpořit", "peníze", "cashflow"],
}

RESPONSE_TEMPLATES = {
    "pozdrav": [
        "Heeej! 🎭 Co se děje, milej? Jak ti letí den?",
        "Čauko čauko! 💋 Zase tady? To mě těší!",
        "Jooo, zdravíííím! ✨ Dneska jsem v pohodě, co ty?",
        "No nazdar! 🔥 Vidím, že jsi tu zase... nemůžeš beze mě být, co? 😏"
    ],
    "kompliment": [
        "Awww, to je od tebe hrozně milý! 🥰 Díky moc!",
        "Ty víš, jak udělat holce radost! 💕 Děkujuuu!",
        "Hehe, tak to ti věřím! 😏 Jsi zlatej!",
        "No jo, já vím... nejsem úplně šeredná 😜 Ale díky!"
    ],
    "obsah": [
        "Už pracuju na novym obsahu, neboj! 📸 Sleduj mě, brzy tu něco bude!",
        "Trpělivost, zlato! 🎬 Chystám něco... zajímavýho. Vyplatí se počkat! 😉",
        "Už mám pár nápadů... ale musíš si ještě chvíli počkat! 🔥",
        "Fotky a videa jsou už na cestě! Jen ještě pár drobností... ✨"
    ],
    "sraz": [
        "Haha, to je milý, ale osobní setkání nedělám! 😅 Radši si mě užívej online! 💻",
        "Aww, chápu, ale já mám radši takový ten... online vztah, víš? 😏",
        "Setkání? Hmmm... možná jednou. Ale zatím jen tady! 🎭",
        "To je sweet návrh, ale pro teď zůstanu v digitálu! 💋"
    ],
    "vulgární": [
        "Ejjj, uklidni se! 😂 Nebav se takhle, jsem tady pro zábavu, ne pro tyhle kecy!",
        "Hele, díky, ale nech si tyhle řeči na později... nebo radši vůbec! 🙄",
        "No to mě pobavilo... ale radši si to nech pro sebe, jo? 😅",
        "Haha, ok ok... ale pojďme mluvit o něčem jinším! 🎭"
    ],
    "dárek": [
        "Ty jsi zlatíčko! 💝 To je od tebe hrozně milý!",
        "Wowww, děkuju moc! 🎁 Tohle mě fakt potěšilo!",
        "Nejseš úžasnej? 💖 Díky za support!",
        "To je tak sweet! 🌟 Opravdu si toho vážím!"
    ],
    "fallback": [
        "Hmmm, to je zajímavá otázka! 🤔 Musím si na to ještě promyslet...",
        "No... tohle je zajímavý! 😅 Možná ti na to odpovím později!",
        "Hehe, nevím, co na to říct! 💭 Ale díky za zprávu!",
        "Zajímavý, ale nejsem si jistá, jak odpovědět! 😊"
    ]
}


def classify_message(msg: str) -> str:
    msg_lower = msg.lower()
    for category, keywords in KEYWORD_MAP.items():
        if any(keyword in msg_lower for keyword in keywords):
            return category
    return "fallback"


def generate_response(msg: str, persona_name: str = "BaddieBabe") -> tuple[str, str]:
    # TODO: napojit na Ollama pro AI generování
    category = classify_message(msg)
    template = random.choice(RESPONSE_TEMPLATES[category])
    return category, template


# Status Generator templates
STATUS_TEMPLATES = {
    "ráno": [
        "Dobré ráno, milí! ☀️ Právě vstávám a už se těším na dnešek! Co vy?",
        "Ranní kávička a já... perfektní začátek dne! ☕✨",
        "Good morning! 🌅 Dneska mám skvělou náladu!",
        "Hej hej, ranní ptáčata! 🐦 Už jste taky vzhůru?"
    ],
    "odpoledne": [
        "Polední chill... 😎 Relaxuju a plánuju večerní content! Co vy?",
        "Odpoledne je čas na trochu pohody! 🌸 Jak se máte?",
        "Užívám si slunce! ☀️ Nádherný den, ne?",
        "Odpolední vibes... 💫 Co plánujete na zbytek dne?"
    ],
    "večer": [
        "Večer je tu! 🌙 Relaxuju u filmečku... Co vy?",
        "Dobrou noc, milí! 🌟 Brzy jdu spát, ale ještě vás pozdravuju!",
        "Večerní nálada... 💜 Jak jste si užili den?",
        "Měla jsem krásný den! 🌃 Doufám, že vy taky!"
    ],
    "náhodný": [
        "Někdy prostě musíte žít teď a tady! ✨ Užívejte si!",
        "Life is good! 💕 Jsem vděčná za každý den!",
        "Dneska mám pocit, že se může stát cokoliv! 🔥",
        "Feeling myself! 💃 Jaká je vaše nálada?"
    ]
}


def get_auto_period() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "ráno"
    elif 12 <= hour < 18:
        return "odpoledne"
    elif 18 <= hour < 23:
        return "večer"
    else:
        return "náhodný"


def generate_status(period: str = "auto") -> str:
    # TODO: napojit na Ollama pro AI generování
    if period == "auto":
        period = get_auto_period()
    templates = STATUS_TEMPLATES.get(period, STATUS_TEMPLATES["náhodný"])
    return random.choice(templates)


def setup_page():
    st.set_page_config(
        page_title="BaddieOS v1.0",
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


def sidebar() -> str:
    with st.sidebar:
        st.markdown("# 🎭 BaddieOS")
        st.markdown("**Command Center v1.0**")
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
        st.markdown("**Verze:** 1.0.0")
        st.markdown("**Status:** 🟢 Online")
        
        return page


def page_dashboard():
    st.title("📊 Dashboard")
    st.markdown("Přehled tvé fanouškovské základny")
    
    df = get_df()
    
    # Metriky
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_fans = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Celkem fanoušků</h3>
            <h1>{total_fans}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        vip_count = len(df[df["tier"] == "VIP"]) if not df.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>👑 VIP</h3>
            <h1>{vip_count}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        supporter_count = len(df[df["tier"] == "Supporter"]) if not df.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>⭐ Supporters</h3>
            <h1>{supporter_count}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_support = df["total_support"].sum() if not df.empty else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Celková podpora</h3>
            <h1>{int(total_support)} Kč</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Top 5 fanoušků
    st.subheader("🏆 Top 5 Fanoušků")
    if not df.empty:
        top5 = df.nlargest(5, "total_support")[["nickname", "tier", "total_support"]]
        for idx, row in top5.iterrows():
            emoji = TIER_EMOJI[row["tier"]]
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"{emoji} **{row['nickname']}**")
            with col2:
                st.markdown(f"*{row['tier']}*")
            with col3:
                st.markdown(f"**{int(row['total_support'])} Kč**")
    else:
        st.info("Zatím žádní fanoušci v databázi.")


def page_crm():
    st.title("👥 CRM & Třídění 'Vojáčků'")
    st.markdown("Správa tvé fanouškovské základny")
    
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
                if not nickname.strip():
                    st.error("Nickname je povinný!")
                else:
                    # Kontrola duplicity
                    existing_fans = load_db()
                    if any(fan["nickname"].lower() == nickname.lower() for fan in existing_fans):
                        st.error(f"Fanoušek '{nickname}' už existuje!")
                    else:
                        new_fan = {
                            "nickname": nickname.strip(),
                            "tier": tier,
                            "total_support": total_support,
                            "notes": notes.strip(),
                            "migrate_telegram": migrate_telegram,
                            "created": datetime.now().isoformat()
                        }
                        existing_fans.append(new_fan)
                        save_db(existing_fans)
                        st.success(f"✅ Fanoušek '{nickname}' byl přidán!")
                        st.rerun()
    
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
                color = TIER_COLORS[row["tier"]]
                
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
                    
                    # Tlačítko pro smazání
                    if st.button(f"🗑️ Smazat {row['nickname']}", key=f"delete_{idx}"):
                        fans_data = load_db()
                        fans_data = [f for f in fans_data if f["nickname"] != row["nickname"]]
                        save_db(fans_data)
                        st.success(f"✅ Fanoušek '{row['nickname']}' byl smazán!")
                        st.rerun()
        else:
            st.info("Žádní fanoušci neodpovídají filtrům.")
    else:
        st.info("Zatím žádní fanoušci v databázi. Přidej prvního pomocí formuláře výše!")


def page_response_assistant():
    st.title("💬 'Inteligentní Provokatérka'")
    st.markdown("AI asistent pro odpovídání na zprávy fanoušků")
    
    # Nastavení persony
    with st.expander("⚙️ Nastavení Persony", expanded=False):
        persona_name = st.text_input("Jméno persony", value="BaddieBabe")
        persona_lore = st.text_area(
            "Persona Lore (background příběh)",
            value="Jsem sebevědomá, trochu drzá, ale vtipná digitální influencerka. Miluji zábavu a komunikaci s fanoušky.",
            height=100
        )
        st.info("💡 **TODO:** V budoucnu se toto napojí na Ollama pro personalizované AI odpovědi.")
    
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
        category, response = generate_response(user_message, persona_name)
        
        st.markdown("---")
        st.subheader("💬 Vygenerovaná odpověď")
        
        st.markdown(f"**Kategorie:** `{category.upper()}`")
        
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


def page_safety_checklist():
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


def page_status_generator():
    st.title("📡 'Teď a Tady' – Status Generator")
    st.markdown("Automatické generování statusů pro sociální sítě")
    
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
            status = generate_status(period)
            st.session_state["single_status"] = status
    
    with col2:
        if st.button("🔄 Generovat 5 statusů"):
            statuses = [generate_status(period) for _ in range(5)]
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
    st.info("💡 **TODO:** V budoucnu se toto napojí na Ollama pro AI generování na míru persony.")


def main():
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
