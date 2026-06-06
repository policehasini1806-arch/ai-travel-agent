"""
General utility helpers for the AI Travel Concierge.
"""
import re
from datetime import datetime


def validate_date(date_str: str) -> bool:
    """Return True if date_str is a valid YYYY-MM-DD date."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def sanitize_input(text: str) -> str:
    """Strip potentially harmful characters from user input."""
    return re.sub(r"[<>\"'%;()&+]", "", text).strip()


def truncate(text: str, max_chars: int = 300) -> str:
    """Truncate text to max_chars, appending '…' if needed."""
    return text if len(text) <= max_chars else text[:max_chars] + "…"


def city_to_iata(city: str) -> str:
    """Very small lookup; expand as needed."""
    mapping = {
        "new york": "JFK",
        "london": "LHR",
        "paris": "CDG",
        "tokyo": "NRT",
        "dubai": "DXB",
        "singapore": "SIN",
        "mumbai": "BOM",
        "delhi": "DEL",
        "bangalore": "BLR",
        "sydney": "SYD",
    }
    return mapping.get(city.lower(), city[:3].upper())


def format_currency(amount: float, symbol: str = "₹") -> str:
    return f"{symbol}{amount:,.0f}"
