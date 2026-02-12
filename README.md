# 🎭 BaddieOS v1.0 – Command Center pro Digitální Provokatérku

```
██████╗  █████╗ ██████╗ ██████╗ ██╗███████╗     ██████╗ ███████╗
██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║██╔════╝    ██╔═══██╗██╔════╝
██████╔╝███████║██║  ██║██║  ██║██║█████╗      ██║   ██║███████╗
██╔══██╗██╔══██║██║  ██║██║  ██║██║██╔══╝      ██║   ██║╚════██║
██████╔╝██║  ██║██████╔╝██████╔╝██║███████╗    ╚██████╔╝███████║
╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝╚══════╝     ╚═════╝ ╚══════╝
```

> **"Není to podvod. Je to performance art s business modelem."**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-brightgreen.svg)]()

---

## 📋 Co to je?

**BaddieOS** je lokální Streamlit dashboard pro profesionální správu fanouškovské základny digitálního influencera na platformě **Amateri.com**. Poskytuje komplexní nástroje pro CRM, komunikaci, bezpečnost obsahu a generování statusů.

### 🎯 Pro koho je to určené?

- 🎭 Digitální influenceři s hybridní identitou (face swap)
- 💼 Malé týmy (2 lidé) s ambiciózními cíli
- 🎪 Kreativci hledající systematický přístup k content creation
- 🔒 Uživatelé, kteří berou privacy vážně

---

## 💰 Business Model

### Whale Hunting Strategie

- **🎯 Cíl:** 50 000 Kč za 3 měsíce
- **👑 Tier systém:**
  - **Free (👤)** – základní fanoušci, potenciální konverze
  - **Supporter (⭐)** – platící fanoušci, 100-500 Kč/měsíc
  - **VIP (👑)** – velryby, 1000+ Kč/měsíc, prioritní komunikace

### Hybrid Identity

- **Face Swap technologie** pro ochranu identity
- **Konzistentní persona** napříč obsahem
- **Privacy-first přístup** – žádné cloud služby

---

## 🏗️ Architektura Projektu

```
provokaterka/
│
├── app.py                    # 🎯 Hlavní Streamlit aplikace
├── ollama_client.py          # 🤖 Ollama API klient (volitelné)
├── requirements.txt          # 📦 Python závislosti
├── .gitignore               # 🚫 Ignorované soubory
│
├── .streamlit/
│   └── config.toml          # 🎨 Dark mode konfigurace
│
├── fans_db.json             # 💾 Lokální JSON databáze (gitignored)
└── README.md                # 📖 Tento soubor
```

---

## 🚀 Instalace & Spuštění na macOS

### Krok 1: Ověř Python

```bash
python3 --version
# Mělo by vypsat: Python 3.10 nebo vyšší
```

Pokud nemáš Python, nainstaluj přes [Homebrew](https://brew.sh/):

```bash
brew install python@3.11
```

### Krok 2: Naklonuj repozitář

```bash
git clone https://github.com/tomasberka/provokaterka.git
cd provokaterka
```

### Krok 3: Nainstaluj závislosti

```bash
pip3 install -r requirements.txt
```

Nebo použij virtuální prostředí (doporučeno):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Krok 4: Spusť aplikaci

```bash
streamlit run app.py
```

Aplikace se otevře v prohlížeči na adrese: **http://localhost:8501**

---

## 🦙 Ollama (Volitelné – AI vylepšení)

BaddieOS je **připravený na Ollama**, ale **funguje i bez něj**! Ollama umožní AI generování textů místo šablon.

### Instalace Ollama na macOS

```bash
# 1. Nainstaluj Ollama
brew install ollama

# 2. Stáhni model (doporučujeme llama3.2)
ollama pull llama3.2

# 3. Spusť Ollama server
ollama serve
```

### Jak to funguje?

- ✅ **BEZ Ollama:** Aplikace používá předpřipravené šablony
- 🤖 **S Ollama:** Aplikace může generovat personalizované odpovědi (připraveno pro budoucí integraci)

**💡 TODO:** Ollama integrace bude aktivována v budoucí verzi pomocí `ollama_client.py`

---

## 📦 Moduly

### 1️⃣ 👥 CRM & Třídění "Vojáčků"

**Správa fanouškovské základny s pokročilými funkcemi.**

**Features:**
- 📊 **JSON databáze** (`fans_db.json`) – lokální, žádný cloud
- 🎯 **3 tier systém** – Free, Supporter, VIP
- 🌈 **Barevné zvýraznění VIP** – okamžitá vizuální identifikace
- ✏️ **CRUD operace** – přidávání, editace, mazání fanoušků
- 🔍 **Filtry** – vyhledávání podle nickname, tier
- 📱 **Telegram checkbox** – označení fanoušků pro migraci

**Sloupce databáze:**
| Sloupec | Typ | Popis |
|---------|-----|-------|
| `nickname` | string | Unikátní přezdívka |
| `tier` | string | Free / Supporter / VIP |
| `total_support` | number | Celková finanční podpora (Kč) |
| `notes` | string | Poznámky k fanouškoví |
| `migrate_telegram` | boolean | Označení pro Telegram migraci |
| `created` | datetime | Datum přidání |

---

### 2️⃣ 💬 "Inteligentní Provokatérka" – Response Assistant

**AI asistent pro odpovídání na zprávy od fanoušků.**

**Features:**
- 🎯 **Keyword klasifikace** – automatické třídění zpráv
- 📚 **7 kategorií:**
  1. 👋 **Pozdrav** – ahoj, nazdar, čau
  2. 💕 **Kompliment** – krásná, sexy, bomba
  3. 📸 **Obsah** – foto, video, nový příspěvek
  4. 🤝 **Sraz** – osobní setkání, meeting
  5. 🔞 **Vulgární** – nevhodné zprávy
  6. 🎁 **Dárek** – support, peníze, gift
  7. 🤷 **Fallback** – ostatní

- 📝 **Šablony odpovědí** – min. 3 varianty pro každou kategorii
- 🎭 **Persona nastavení** – jméno, background lore
- 🤖 **Připraveno na Ollama** – budoucí AI generování

**Příklad použití:**
1. Vlož zprávu od fanouška
2. Klikni "Generovat odpověď"
3. Systém klasifikuje zprávu a nabídne odpověď
4. Zkopíruj a pošli

---

### 3️⃣ 🔒 Content Manager & Bezpečnost

**5-bodový checklist před uploadem obsahu – ochrana identity.**

**Safety Checklist:**

✅ **1. Metadata odstraněna**
- EXIF data (GPS, datum, model fotoaparátu)
- Použij nástroje: `exiftool`, `ImageOptim`

✅ **2. Pozadí neutrální**
- Žádné identifikovatelné lokace
- Neutrální pozadí nebo rozmazání

✅ **3. Žádné identifikační znaky**
- Tetování, znaménka, šperky
- Kontrola každého detailu

✅ **4. Face swap aplikován**
- Přirozený výsledek
- Kontrola rozlišení a světla

✅ **5. Tón pleti konzistentní**
- Shoduje se s předchozím obsahem
- Stejné osvětlení

**Výsledek:**
- 🟢 **5/5 bodů** → `✅ SAFE TO UPLOAD` + 🎈 balloons
- 🔴 **< 5 bodů** → `⚠️ UNSAFE` – nenahávej!

---

### 4️⃣ 📡 "Teď a Tady" – Status Generator

**Automatické generování statusů pro sociální sítě podle denního období.**

**Features:**
- ⏰ **Auto-detekce období** podle aktuálního času:
  - 🌅 **Ráno** (5:00 - 12:00)
  - ☀️ **Odpoledne** (12:00 - 18:00)
  - 🌙 **Večer** (18:00 - 23:00)
  - 🎲 **Náhodný** (ostatní časy)

- 📝 **Šablony statusů** – min. 4 varianty pro každé období
- 🎲 **Generovat 1** – jeden náhodný status
- 🔄 **Generovat 5** – dávka statusů najednou
- 📋 **Kopírování** – `st.code()` box pro snadné copy-paste
- 🤖 **Připraveno na Ollama** – budoucí personalizace

**Příklad šablon:**

**Ráno:**
> "Dobré ráno, milí! ☀️ Právě vstávám a už se těším na dnešek! Co vy?"

**Odpoledne:**
> "Polední chill... 😎 Relaxuju a plánuju večerní content! Co vy?"

**Večer:**
> "Večer je tu! 🌙 Relaxuju u filmečku... Co vy?"

---

## 🔐 Bezpečnost & Soukromí

### 🏠 100% Lokální

- ✅ **Žádné cloud API** – vše běží na tvém počítači
- ✅ **JSON gitignored** – `fans_db.json` není v Gitu
- ✅ **Privacy-first** – žádná data se nikam neodesílají
- ✅ **Offline funkční** – nepotřebuješ internet (kromě instalace)

### 🔒 Best Practices

- 🔐 Necommituj `fans_db.json` do Gitu
- 🗑️ Pravidelně zálohuj databázi offline
- 🛡️ Používej VPN při nahrávání obsahu
- 🔑 Nikdy nesdílej `.streamlit/secrets.toml` (pokud používáš)

---

## 🛠️ Tech Stack

| Technologie | Verze | Účel |
|------------|-------|------|
| **Python** | 3.10+ | Backend logika |
| **Streamlit** | 1.30+ | Web UI framework |
| **Pandas** | 2.0+ | Data manipulace |
| **Ollama** | Latest | AI generování (volitelné) |
| **JSON** | - | Lokální databáze |

---

## 🗺️ Roadmap

Plánované funkce pro budoucí verze:

- [ ] 🤖 **Ollama integrace** – AI generování odpovědí a statusů
- [ ] 💾 **SQLite migrace** – výkonnější databáze
- [ ] 📊 **Export do CSV** – záloha a analýza dat
- [ ] 📈 **Analytika** – grafy, statistiky, trendy
- [ ] 📱 **Telegram bot** – automatické odpovídání
- [ ] 🎭 **Multi-persona** – správa více identit
- [ ] ⏰ **Cron scheduling** – automatické posty
- [ ] 🔔 **Notifikace** – upozornění na nové zprávy
- [ ] 🌐 **i18n** – podpora více jazyků
- [ ] 🔌 **API integrace** – propojení s Amateri.com

---

## ⚠️ Disclaimer

**BaddieOS je edukační nástroj** pro pochopení business modelů v digitálním prostředí. Uživatelé jsou plně zodpovědní za způsob, jakým nástroj používají. Autoři nenese odpovědnost za zneužití nebo porušení podmínek třetích stran.

**Důležité:**
- ✅ Vždy dodržuj **Terms of Service** platformy, kterou používáš
- ✅ Respektuj **privacy** všech zúčastněných
- ✅ Používej face swap **eticky a legálně**
- ✅ Neklaměj o skutečné identitě tam, kde je to zakázáno

---

## 📄 Licence

**MIT License** – volně použitelné, upravitelné, distribuovatelné.

```
Copyright (c) 2026 Tomáš Berka

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🤝 Podpora

Máš problém nebo nápad na vylepšení?

- 🐛 **Issue:** [GitHub Issues](https://github.com/tomasberka/provokaterka/issues)
- 💡 **Feature Request:** Otevři diskuzi v Issues
- 📧 **Kontakt:** Přes GitHub profil

---

## 🎉 Acknowledgments

- 🎨 Inspirováno moderními CRM systémy
- 🤖 Připraveno pro AI revoluci (Ollama)
- 💜 Děkujeme komunitě Streamlit
- 🔒 Privacy-first filosofie

---

<div align="center">

**🎭 BaddieOS v1.0 – Performance Art s Business Modelem 🎭**

Made with 💙 for digital creators

</div>
