"""
Databázová vrstva pro BaddieOS.
Správa fanouškovské databáze v JSON formátu.
"""

import json
import os
import csv
import io
from datetime import datetime
from typing import Optional

import pandas as pd

from config import DB_FILE, DB_COLUMNS


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


def add_fan(nickname: str, tier: str, total_support: int = 0,
            notes: str = "", migrate_telegram: bool = False) -> tuple[bool, str]:
    """
    Přidá nového fanouška. Vrátí (success, message).
    """
    if not nickname.strip():
        return False, "Nickname je povinný!"

    fans = load_db()
    if any(fan["nickname"].lower() == nickname.strip().lower() for fan in fans):
        return False, f"Fanoušek '{nickname}' už existuje!"

    new_fan = {
        "nickname": nickname.strip(),
        "tier": tier,
        "total_support": total_support,
        "notes": notes.strip(),
        "migrate_telegram": migrate_telegram,
        "created": datetime.now().isoformat()
    }
    fans.append(new_fan)
    save_db(fans)
    return True, f"✅ Fanoušek '{nickname}' byl přidán!"


def update_fan(original_nickname: str, tier: Optional[str] = None,
               total_support: Optional[int] = None, notes: Optional[str] = None,
               migrate_telegram: Optional[bool] = None) -> tuple[bool, str]:
    """
    Aktualizuje existujícího fanouška. Vrátí (success, message).
    """
    fans = load_db()
    for fan in fans:
        if fan["nickname"] == original_nickname:
            if tier is not None:
                fan["tier"] = tier
            if total_support is not None:
                fan["total_support"] = total_support
            if notes is not None:
                fan["notes"] = notes
            if migrate_telegram is not None:
                fan["migrate_telegram"] = migrate_telegram
            save_db(fans)
            return True, f"✅ Fanoušek '{original_nickname}' byl aktualizován!"
    return False, f"Fanoušek '{original_nickname}' nebyl nalezen!"


def delete_fan(nickname: str) -> tuple[bool, str]:
    """Smaže fanouška. Vrátí (success, message)."""
    fans = load_db()
    new_fans = [f for f in fans if f["nickname"] != nickname]
    if len(new_fans) == len(fans):
        return False, f"Fanoušek '{nickname}' nebyl nalezen!"
    save_db(new_fans)
    return True, f"✅ Fanoušek '{nickname}' byl smazán!"


def export_csv() -> str:
    """Exportuje databázi do CSV formátu (vrátí string)."""
    fans = load_db()
    if not fans:
        return ""

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=DB_COLUMNS)
    writer.writeheader()
    for fan in fans:
        row = {col: fan.get(col, "") for col in DB_COLUMNS}
        writer.writerow(row)
    return output.getvalue()
