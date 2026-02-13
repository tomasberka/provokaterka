"""
Testy pro BaddieOS – klasifikace zpráv, generování odpovědí,
databázové operace a CSV export.
"""

import json
import os
import tempfile
from unittest import mock

import pytest

# Redirect DB_FILE to a temp file before importing modules
_tmp_db = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
_tmp_db.close()

import config
config.DB_FILE = _tmp_db.name

from responses import classify_message, generate_response, get_auto_period, generate_status
from database import load_db, save_db, get_df, add_fan, update_fan, delete_fan, export_csv
from config import KEYWORD_MAP, RESPONSE_TEMPLATES, STATUS_TEMPLATES, TIERS


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(autouse=True)
def clean_db():
    """Vyčistí databázi před každým testem."""
    config.DB_FILE = _tmp_db.name
    with open(config.DB_FILE, "w") as f:
        json.dump([], f)
    yield
    # Cleanup
    if os.path.exists(config.DB_FILE):
        with open(config.DB_FILE, "w") as f:
            json.dump([], f)


# ============================================================================
# TESTY: KLASIFIKACE ZPRÁV
# ============================================================================

class TestClassifyMessage:
    """Testy pro classify_message()."""

    def test_classify_pozdrav(self):
        assert classify_message("Ahoj, jak se máš?") == "pozdrav"
        assert classify_message("Nazdar!") == "pozdrav"
        assert classify_message("Čau krásko") == "pozdrav"

    def test_classify_kompliment(self):
        assert classify_message("Jsi nádherná!") == "kompliment"
        assert classify_message("Vypadáš sexy") == "kompliment"
        assert classify_message("Jsi bomba") == "kompliment"

    def test_classify_obsah(self):
        assert classify_message("Kdy bude nový foto?") == "obsah"
        assert classify_message("Máš nové video?") == "obsah"

    def test_classify_sraz(self):
        assert classify_message("Můžeme se potkat?") == "sraz"
        assert classify_message("Sejdeme se osobně?") == "sraz"

    def test_classify_darek(self):
        assert classify_message("Chci tě podpořit!") == "dárek"
        assert classify_message("Poslal jsem ti gift") == "dárek"

    def test_classify_fallback(self):
        assert classify_message("Jaké je počasí?") == "fallback"
        assert classify_message("xyz abc 123") == "fallback"

    def test_classify_case_insensitive(self):
        assert classify_message("AHOJ") == "pozdrav"
        assert classify_message("SEXY") == "kompliment"


# ============================================================================
# TESTY: GENEROVÁNÍ ODPOVĚDÍ
# ============================================================================

class TestGenerateResponse:
    """Testy pro generate_response()."""

    def test_returns_tuple(self):
        result = generate_response("Ahoj!")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_valid_category(self):
        category, response = generate_response("Ahoj!")
        assert category in RESPONSE_TEMPLATES

    def test_response_is_from_templates(self):
        category, response = generate_response("Ahoj!")
        assert response in RESPONSE_TEMPLATES[category]

    def test_fallback_response(self):
        category, response = generate_response("random nonsense xyz")
        assert category == "fallback"
        assert response in RESPONSE_TEMPLATES["fallback"]


# ============================================================================
# TESTY: GENEROVÁNÍ STATUSŮ
# ============================================================================

class TestGenerateStatus:
    """Testy pro generate_status()."""

    def test_specific_period(self):
        status = generate_status("ráno")
        assert status in STATUS_TEMPLATES["ráno"]

    def test_unknown_period_uses_nahodny(self):
        status = generate_status("neexistujici")
        assert status in STATUS_TEMPLATES["náhodný"]

    def test_auto_period(self):
        status = generate_status("auto")
        # Should return a valid status from one of the periods
        all_statuses = []
        for templates in STATUS_TEMPLATES.values():
            all_statuses.extend(templates)
        assert status in all_statuses


class TestGetAutoPeriod:
    """Testy pro get_auto_period()."""

    def test_morning(self):
        with mock.patch("responses.datetime") as mock_dt:
            mock_dt.now.return_value.hour = 8
            assert get_auto_period() == "ráno"

    def test_afternoon(self):
        with mock.patch("responses.datetime") as mock_dt:
            mock_dt.now.return_value.hour = 14
            assert get_auto_period() == "odpoledne"

    def test_evening(self):
        with mock.patch("responses.datetime") as mock_dt:
            mock_dt.now.return_value.hour = 20
            assert get_auto_period() == "večer"

    def test_night(self):
        with mock.patch("responses.datetime") as mock_dt:
            mock_dt.now.return_value.hour = 2
            assert get_auto_period() == "náhodný"


# ============================================================================
# TESTY: DATABÁZOVÉ OPERACE
# ============================================================================

class TestDatabase:
    """Testy pro databázové operace."""

    def test_load_empty_db(self):
        result = load_db()
        assert result == []

    def test_save_and_load(self):
        data = [{"nickname": "TestFan", "tier": "VIP", "total_support": 1000}]
        save_db(data)
        loaded = load_db()
        assert len(loaded) == 1
        assert loaded[0]["nickname"] == "TestFan"

    def test_add_fan_success(self):
        success, msg = add_fan("NewFan", "Free", 0, "test notes", False)
        assert success is True
        fans = load_db()
        assert len(fans) == 1
        assert fans[0]["nickname"] == "NewFan"

    def test_add_fan_duplicate(self):
        add_fan("Duplicate", "Free")
        success, msg = add_fan("Duplicate", "VIP")
        assert success is False

    def test_add_fan_empty_nickname(self):
        success, msg = add_fan("", "Free")
        assert success is False

    def test_add_fan_case_insensitive_duplicate(self):
        add_fan("TestFan", "Free")
        success, msg = add_fan("testfan", "VIP")
        assert success is False

    def test_update_fan(self):
        add_fan("UpdateMe", "Free", 0)
        success, msg = update_fan("UpdateMe", tier="VIP", total_support=500)
        assert success is True
        fans = load_db()
        assert fans[0]["tier"] == "VIP"
        assert fans[0]["total_support"] == 500

    def test_update_nonexistent_fan(self):
        success, msg = update_fan("NoSuchFan", tier="VIP")
        assert success is False

    def test_delete_fan(self):
        add_fan("DeleteMe", "Free")
        success, msg = delete_fan("DeleteMe")
        assert success is True
        assert load_db() == []

    def test_delete_nonexistent_fan(self):
        success, msg = delete_fan("NoSuchFan")
        assert success is False

    def test_get_df_empty(self):
        df = get_df()
        assert len(df) == 0

    def test_get_df_with_data(self):
        add_fan("Fan1", "VIP", 1000)
        add_fan("Fan2", "Free", 0)
        df = get_df()
        assert len(df) == 2


# ============================================================================
# TESTY: CSV EXPORT
# ============================================================================

class TestExportCSV:
    """Testy pro CSV export."""

    def test_export_empty(self):
        result = export_csv()
        assert result == ""

    def test_export_with_data(self):
        add_fan("CSVFan", "Supporter", 250, "test note", True)
        csv_str = export_csv()
        assert "CSVFan" in csv_str
        assert "Supporter" in csv_str
        assert "nickname" in csv_str  # header row

    def test_export_multiple_fans(self):
        add_fan("Fan1", "Free", 0)
        add_fan("Fan2", "VIP", 5000)
        csv_str = export_csv()
        lines = csv_str.strip().split("\n")
        assert len(lines) == 3  # header + 2 data rows
