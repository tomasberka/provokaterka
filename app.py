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


# ============================================================================
# DATABÁZOVÁ VRSTVA
# ============================================================================

DB_FILE = "fans_db.json"
DB_COLUMNS = ["nickname", "tier", "total_support", "notes", "migrate_telegram", "created"]


def load_db() -> list:
    """Načte databázi fanoušků z JSON souboru."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_db(data: list) -> None:
    """Uloží databázi fanoušků do JSON souboru."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_df() -> pd.DataFrame:
    """Vrátí DataFrame s fanoušky."""
    data = load_db()
    if not data:
        return pd.DataFrame(columns=DB_COLUMNS)
    return pd.DataFrame(data)


# ============================================================================
# KONSTANTY
# ============================================================================

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


# ============================================================================
# ŠABLONY PRO RESPONSE ASSISTANT
# ============================================================================

# Kategorie zpráv s klíčovými slovy
KEYWORD_MAP = {
    "pozdrav": ["ahoj", "nazdar", "čau", "zdravím", "dobrý", "hej", "halo"],
    "kompliment": ["krásná", "nádherná", "sexy", "parádní", "úžasná", "bomba", "kráska", "líbíš"],
    "obsah": ["foto", "fotka", "video", "obsah", "příspěvek", "nový", "kdy", "ukáž"],
    "sraz": ["sraz", "meeting", "osobně", "potkat", "vidět", "sejít", "sejdeme"],
    "vulgární": ["sex", "prd", "kunda", "pica", "péro", "šukat", "píča"],
    "dárek": ["dárek", "gift", "poslat", "support", "podpořit", "peníze", "cashflow"],
}

# Šablony odpovědí pro každou kategorii
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
    """Klasifikuje zprávu podle klíčových slov."""
    msg_lower = msg.lower()
    for category, keywords in KEYWORD_MAP.items():
        if any(keyword in msg_lower for keyword in keywords):
            return category
    return "fallback"


def generate_response(msg: str, persona_name: str = "BaddieBabe") -> tuple[str, str]:
    """
    Generuje odpověď na zprávu.
    TODO: V budoucnu napojit na Ollama pro AI generování.
    """
    category = classify_message(msg)
    template = random.choice(RESPONSE_TEMPLATES[category])
    return category, template


# ============================================================================
# ŠABLONY PRO STATUS GENERATOR
# ============================================================================

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


def generate_status(period: str = "auto") -> str:
    """
    Vygeneruje status pro zvolené období.
    TODO: V budoucnu napojit na Ollama pro AI generování.
    """
    if period == "auto":
        period = get_auto_period()
    templates = STATUS_TEMPLATES.get(period, STATUS_TEMPLATES["náhodný"])
    return random.choice(templates)


# ============================================================================
# COMFYUI PIPELINE – GENERÁTOR WORKFLOW
# ============================================================================

def generate_comfyui_workflow(
    breed: str,
    positive_prompt: str,
    negative_prompt: str,
    controlnet_strength: float,
    ip_adapter_weight: float,
    steps: int,
    cfg: float,
    seed: int,
    width: int,
    height: int,
    frame_rate: int,
    total_frames: int,
) -> dict:
    """
    Generuje ComfyUI API workflow JSON pro tancujícího psa.
    Pipeline: DWPose ControlNet → IP-Adapter Plus → AnimateDiff → Tile Upscale.
    """
    workflow = {
        "1": {
            "inputs": {"ckpt_name": "realisticVisionV60B1_v51VAE.safetensors"},
            "class_type": "CheckpointLoaderSimple",
            "_meta": {"title": "Načíst základní model"}
        },
        "2": {
            "inputs": {
                "video": "input_dance.mp4",
                "force_rate": frame_rate,
                "force_size": "Disabled",
                "frame_load_cap": total_frames,
                "skip_first_frames": 0,
                "select_every_nth": 1
            },
            "class_type": "VHS_LoadVideo",
            "_meta": {"title": "Načíst taneční video"}
        },
        "3": {
            "inputs": {
                "detect_hand": "enable",
                "detect_body": "enable",
                "detect_face": "enable",
                "resolution": width,
                "image": ["2", 0]
            },
            "class_type": "DWPreprocessor",
            "_meta": {"title": "DWPose – extrakce pohybu"}
        },
        "4": {
            "inputs": {"control_net_name": "control_v11p_sd15_openpose_fp16.safetensors"},
            "class_type": "ControlNetLoader",
            "_meta": {"title": "Načíst DWPose ControlNet"}
        },
        "5": {
            "inputs": {
                "strength": controlnet_strength,
                "start_percent": 0.0,
                "end_percent": 1.0,
                "positive": ["6", 0],
                "negative": ["6", 1],
                "control_net": ["4", 0],
                "image": ["3", 0]
            },
            "class_type": "ControlNetApplyAdvanced",
            "_meta": {"title": f"Aplikovat ControlNet (síla: {controlnet_strength})"}
        },
        "6": {
            "inputs": {
                "text": positive_prompt,
                "clip": ["1", 1]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "Pozitivní prompt"}
        },
        "7": {
            "inputs": {
                "text": negative_prompt,
                "clip": ["1", 1]
            },
            "class_type": "CLIPTextEncode",
            "_meta": {"title": "Negativní prompt"}
        },
        "8": {
            "inputs": {"image": "dog_photo.png", "upload": "image"},
            "class_type": "LoadImage",
            "_meta": {"title": "Načíst fotku psa"}
        },
        "9": {
            "inputs": {
                "ipadapter_file": "ip-adapter-plus_sd15.bin"
            },
            "class_type": "IPAdapterModelLoader",
            "_meta": {"title": "Načíst IP-Adapter Plus model"}
        },
        "10": {
            "inputs": {
                "weight": ip_adapter_weight,
                "weight_type": "original",
                "start_at": 0.0,
                "end_at": 1.0,
                "combine_embeds": "concat",
                "embeds_scaling": "V only",
                "model": ["1", 0],
                "ipadapter": ["9", 0],
                "image": ["8", 0]
            },
            "class_type": "IPAdapterAdvanced",
            "_meta": {"title": f"IP-Adapter Plus (váha: {ip_adapter_weight})"}
        },
        "11": {
            "inputs": {
                "model_name": "mm_sd_v15_v2.ckpt",
                "beta_schedule": "linear (AnimateDiff)"
            },
            "class_type": "AnimateDiffLoaderWithContext",
            "_meta": {"title": "AnimateDiff V2 – časová konzistence"}
        },
        "12": {
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": "euler_ancestral",
                "scheduler": "karras",
                "denoise": 1.0,
                "model": ["11", 0],
                "positive": ["5", 0],
                "negative": ["5", 1],
                "latent_image": ["13", 0]
            },
            "class_type": "KSampler",
            "_meta": {"title": "KSampler – generování"}
        },
        "13": {
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": total_frames
            },
            "class_type": "EmptyLatentImage",
            "_meta": {"title": "Prázdný latentní prostor"}
        },
        "14": {
            "inputs": {
                "samples": ["12", 0],
                "vae": ["1", 2]
            },
            "class_type": "VAEDecode",
            "_meta": {"title": "VAE Decode"}
        },
        "15": {
            "inputs": {
                "upscale_model": "RealESRGAN_x2plus.pth"
            },
            "class_type": "UpscaleModelLoader",
            "_meta": {"title": "Načíst Upscale model"}
        },
        "16": {
            "inputs": {
                "upscale_model": ["15", 0],
                "image": ["14", 0]
            },
            "class_type": "ImageUpscaleWithModel",
            "_meta": {"title": "Tile Upscale – zvýšení rozlišení"}
        },
        "17": {
            "inputs": {
                "frame_rate": frame_rate,
                "loop_count": 0,
                "filename_prefix": f"dog_dance_{breed.replace(' ', '_')}",
                "format": "video/h264-mp4",
                "pix_fmt": "yuv420p",
                "crf": 19,
                "save_metadata": True,
                "pingpong": False,
                "save_output": True,
                "images": ["16", 0]
            },
            "class_type": "VHS_VideoCombine",
            "_meta": {"title": "Uložit výsledné video"}
        }
    }
    return workflow


# ============================================================================
# SETUP & STYLING
# ============================================================================

def setup_page():
    """Nastaví stránku a custom CSS."""
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


# ============================================================================
# SIDEBAR NAVIGACE
# ============================================================================

def sidebar() -> str:
    """Zobrazí sidebar s navigací."""
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
                "📡 Status Generator",
                "🎬 ComfyUI Pipeline"
            ]
        )
        
        st.markdown("---")
        st.markdown("**Verze:** 1.0.0")
        st.markdown("**Status:** 🟢 Online")
        
        return page


# ============================================================================
# STRÁNKA: DASHBOARD
# ============================================================================

def page_dashboard():
    """Hlavní dashboard s přehledem metrik."""
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


# ============================================================================
# STRÁNKA: CRM & TŘÍDĚNÍ VOJÁČKŮ
# ============================================================================

def page_crm():
    """CRM modul pro správu fanoušků."""
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


# ============================================================================
# STRÁNKA: RESPONSE ASSISTANT
# ============================================================================

def page_response_assistant():
    """Modul pro generování odpovědí na zprávy."""
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


# ============================================================================
# STRÁNKA: SAFETY CHECKLIST
# ============================================================================

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


# ============================================================================
# STRÁNKA: STATUS GENERATOR
# ============================================================================

def page_status_generator():
    """Modul pro generování statusů."""
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


# ============================================================================
# STRÁNKA: COMFYUI PIPELINE
# ============================================================================

def page_comfyui_pipeline():
    """Modul pro konfiguraci a export ComfyUI workflow pro tančícího psa."""
    st.title("🎬 ComfyUI Pipeline – Tančící Pes")
    st.markdown("Konfigurátor workflow pro generování videa psa tančícího podle lidského vzoru")

    # Přehled pipeline
    st.markdown("---")
    st.subheader("🗺️ Pipeline přehled")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>1️⃣</h3>
            <p><strong>DWPose</strong></p>
            <p>Extrakce pohybu</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>2️⃣</h3>
            <p><strong>IP-Adapter</strong></p>
            <p>Identita psa</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>3️⃣</h3>
            <p><strong>AnimateDiff</strong></p>
            <p>Časová konzistence</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>4️⃣</h3>
            <p><strong>Prompt</strong></p>
            <p>Engineering</p>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div class="metric-card">
            <h3>5️⃣</h3>
            <p><strong>Upscale</strong></p>
            <p>Post-produkce</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Krok 1 – DWPose ControlNet
    with st.expander("1️⃣ Extrakce pohybu – DWPose ControlNet", expanded=True):
        st.markdown("""
        **Proč DWPose a ne klasický OpenPose?**
        DWPose (DWPreprocessor) je výrazně přesnější v detekci rukou a složitých póz – ideální pro taneční pohyby.

        - 📥 **Vstup:** Referenční TikTok video s tancem
        - ⚙️ **Proces:** DWPose vyextrahuje z tancujícího člověka "stickmana" – kostru pohybu
        - 🐾 **Trik:** Pes nemá lidská kolena → sniž `strength` na 0.7–0.8, aby AI mohla přizpůsobit psí anatomii
        """)
        controlnet_strength = st.slider(
            "ControlNet Strength",
            min_value=0.0, max_value=1.0,
            value=0.75, step=0.05,
            help="Doporučená hodnota: 0.70–0.80 pro psí anatomii"
        )
        st.caption(f"✅ Vybrána síla: **{controlnet_strength}** – {'🐾 Vhodné pro psa' if 0.65 <= controlnet_strength <= 0.85 else '⚠️ Mimo doporučený rozsah'}")

    # Krok 2 – IP-Adapter
    with st.expander("2️⃣ Zachování identity psa – IP-Adapter Plus", expanded=True):
        st.markdown("""
        **Proč IP-Adapter místo LoRA?**
        IP-Adapter Plus nevyžaduje trénování – stačí jedna čistá fotka psa.

        - 📥 **Vstup:** Fotka psa (ideálně pohled přímo do kamery)
        - 🎨 **Výsledek:** AI převezme texturu srsti, barvy a tvar obličeje
        - 💡 **Tip:** Pro velmi specifické psy přidej druhý pass přes IP-Adapter FaceID zaměřený jen na čumák
        """)
        ip_adapter_weight = st.slider(
            "IP-Adapter Weight",
            min_value=0.0, max_value=1.5,
            value=0.85, step=0.05,
            help="Vyšší hodnota = silnější vliv fotky psa na výsledek"
        )
        st.caption(f"✅ Vybrána váha: **{ip_adapter_weight}**")

    # Krok 3 – AnimateDiff
    with st.expander("3️⃣ Časová konzistence – AnimateDiff", expanded=True):
        st.markdown("""
        **Proč AnimateDiff?**
        Zabraňuje blikání a "třesu" mezi snímky – pes se během celého tance nebude měnit na jiné plemeno.

        - ✅ Doporučené modely: **V2** nebo **V3** pro nejlepší plynulost
        - 🎞️ Uzamyká kontext mezi jednotlivými framy
        """)
        col1, col2 = st.columns(2)
        with col1:
            total_frames = st.number_input(
                "Počet framů", min_value=8, max_value=128,
                value=24, step=8,
                help="Doporučeno: 16–32 framů pro plynulou animaci"
            )
        with col2:
            frame_rate = st.number_input(
                "Frame rate (FPS)", min_value=8, max_value=30,
                value=16, step=1
            )
        st.caption(f"🎬 Délka videa: cca **{total_frames / frame_rate:.1f}s** při {frame_rate} FPS")

    # Krok 4 – Prompt Engineering
    with st.expander("4️⃣ Prompt Engineering", expanded=True):
        st.markdown("""
        **Klíčová slova pro propojení lidské kostry s psím tělem:**
        - `anthropomorphic` nebo `standing upright` dává AI povolení aplikovat DWPose kostru na zvíře
        """)
        breed = st.text_input(
            "Plemeno psa",
            value="golden retriever",
            help="Např. golden retriever, german shepherd, husky..."
        )
        positive_prompt = st.text_area(
            "Pozitivní prompt",
            value=f"anthropomorphic {breed} dog, standing upright on two hind legs, dancing, human-like posture, highly detailed, realistic lighting, 4k, volumetric light",
            height=80
        )
        negative_prompt = st.text_area(
            "Negativní prompt",
            value="blurry, deformed limbs, extra legs, unnatural pose, low quality, watermark, cartoon",
            height=60
        )

    # Krok 5 – Post-produkce
    with st.expander("5️⃣ Post-produkce & Upscale", expanded=True):
        st.markdown("""
        **Výstup z AnimateDiff bývá v nižším rozlišení – pro ostré video na sociální sítě ho upscaluj.**

        - 🔲 **Tile ControlNet Upscale** – zachová detaily srsti
        - 📱 **Výstupní formát:** Vertikální 9:16 pro Reels/TikTok
        - 🎵 **Tip:** Přilep moderní energický beat a máš hotovo!
        """)
        col1, col2 = st.columns(2)
        with col1:
            width = st.selectbox("Šířka (px)", [512, 576, 640, 768], index=1)
        with col2:
            height = st.selectbox("Výška (px)", [768, 896, 1024], index=0)
        st.caption(f"📐 Poměr stran: **{width}×{height}** (~{height/width:.2f}:1)")

    # Pokročilé nastavení
    with st.expander("⚙️ Pokročilé nastavení sampleru"):
        col1, col2, col3 = st.columns(3)
        with col1:
            steps = st.slider("Kroky sampleru", min_value=10, max_value=50, value=25, step=5)
        with col2:
            cfg = st.slider("CFG Scale", min_value=1.0, max_value=15.0, value=7.5, step=0.5)
        with col3:
            seed = st.number_input("Seed (0 = náhodný)", min_value=0, max_value=2**31 - 1,
                                   value=0, step=1)

    st.markdown("---")

    # Generování a stažení workflow
    st.subheader("📦 Export ComfyUI Workflow")
    st.info("""
    💡 **Jak použít:**
    1. Zkonfiguruj parametry výše
    2. Klikni **Generovat workflow**
    3. Stáhni JSON a importuj do ComfyUI (drag & drop do okna)
    4. Nahraj `input_dance.mp4` a `dog_photo.png` do složky `ComfyUI/input/`
    5. Klikni **Queue Prompt** – a sekáš obsah jako Baťa cvičky 🎉
    """)

    if st.button("⚡ Generovat ComfyUI Workflow JSON", type="primary"):
        effective_seed = seed if seed != 0 else random.randint(1, 2**31 - 1)
        workflow = generate_comfyui_workflow(
            breed=breed,
            positive_prompt=positive_prompt,
            negative_prompt=negative_prompt,
            controlnet_strength=controlnet_strength,
            ip_adapter_weight=ip_adapter_weight,
            steps=steps,
            cfg=cfg,
            seed=effective_seed,
            width=width,
            height=height,
            frame_rate=frame_rate,
            total_frames=total_frames,
        )
        workflow_json = json.dumps(workflow, ensure_ascii=False, indent=2)

        st.success("✅ Workflow vygenerováno!")
        st.download_button(
            label="⬇️ Stáhnout workflow.json",
            data=workflow_json,
            file_name=f"dog_dance_{breed.replace(' ', '_')}_workflow.json",
            mime="application/json"
        )

        # Náhled JSON
        with st.expander("🔍 Náhled workflow JSON"):
            st.code(workflow_json, language="json")

    st.markdown("---")

    # Přehled potřebných modelů
    st.subheader("📋 Potřebné modely & rozšíření")
    st.markdown("""
    | Komponenta | Soubor | Složka v ComfyUI |
    |-----------|--------|-----------------|
    | Base model | `realisticVisionV60B1_v51VAE.safetensors` | `models/checkpoints/` |
    | DWPose ControlNet | `control_v11p_sd15_openpose_fp16.safetensors` | `models/controlnet/` |
    | IP-Adapter Plus | `ip-adapter-plus_sd15.bin` | `models/ipadapter/` |
    | AnimateDiff V2 | `mm_sd_v15_v2.ckpt` | `custom_nodes/ComfyUI-AnimateDiff-Evolved/models/` |
    | Upscale | `RealESRGAN_x2plus.pth` | `models/upscale_models/` |
    | **Rozšíření** | ComfyUI-AnimateDiff-Evolved | `custom_nodes/` |
    | **Rozšíření** | ComfyUI-VideoHelperSuite | `custom_nodes/` |
    | **Rozšíření** | ComfyUI_IPAdapter_plus | `custom_nodes/` |
    | **Rozšíření** | comfyui_controlnet_aux | `custom_nodes/` |
    """)


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
    elif page == "🎬 ComfyUI Pipeline":
        page_comfyui_pipeline()


if __name__ == "__main__":
    main()
