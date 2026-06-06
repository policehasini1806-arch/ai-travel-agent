"""
Basic test suite for the AI Travel Concierge.
Run with: pytest tests/
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from utils.helpers import validate_date, sanitize_input, truncate, city_to_iata, format_currency
from backend.database import init_db, save_search, get_search_history, clear_history


# ── Helpers ────────────────────────────────────────────────────────────────────

def test_validate_date_valid():
    assert validate_date("2025-08-15") is True

def test_validate_date_invalid():
    assert validate_date("15-08-2025") is False
    assert validate_date("not-a-date") is False

def test_sanitize_input_strips_chars():
    assert sanitize_input("<script>alert(1)</script>") == "scriptalert1/script"

def test_sanitize_input_clean():
    assert sanitize_input("  Paris, France  ") == "Paris, France"

def test_truncate_short():
    assert truncate("Hello", 100) == "Hello"

def test_truncate_long():
    result = truncate("A" * 400, 300)
    assert result.endswith("…")
    assert len(result) == 301  # 300 chars + ellipsis

def test_city_to_iata_known():
    assert city_to_iata("london") == "LHR"
    assert city_to_iata("Tokyo") == "NRT"

def test_city_to_iata_unknown():
    assert city_to_iata("Bengaluru") == "BEN"

def test_format_currency():
    assert format_currency(5000) == "₹5,000"
    assert format_currency(1234567, "$") == "$1,234,567"


# ── Database ───────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def use_temp_db(tmp_path, monkeypatch):
    """Redirect the DB to a temp directory for each test."""
    monkeypatch.setattr("backend.database.DB_PATH", str(tmp_path / "test.db"))
    init_db()
    yield
    clear_history()

def test_save_and_retrieve():
    save_search("best beaches in Goa", "Here are the top beaches…")
    history = get_search_history()
    assert len(history) == 1
    assert history[0]["query"] == "best beaches in Goa"

def test_history_newest_first():
    save_search("query 1", "response 1")
    save_search("query 2", "response 2")
    history = get_search_history()
    assert history[0]["query"] == "query 2"

def test_clear_history():
    save_search("temp query", "temp response")
    clear_history()
    assert get_search_history() == []

def test_history_limit():
    for i in range(10):
        save_search(f"query {i}", f"response {i}")
    history = get_search_history(limit=5)
    assert len(history) == 5
