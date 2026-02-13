"""
Konfigurace a konstanty pro BaddieOS.
"""

DB_FILE = "fans_db.json"
DB_COLUMNS = ["nickname", "tier", "total_support", "notes", "migrate_telegram", "created"]

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

# Šablony statusů
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
