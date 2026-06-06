import os
import requests
from langchain_core.tools import tool


@tool
def weather_tool(location: str) -> str:
    """Get current weather for a city. Input: city name like 'Hyderabad' or 'Paris'."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return f"Weather API key not configured. Sample: {location} is 32°C, Sunny."
    try:
        resp = requests.get(
            "http://api.weatherapi.com/v1/forecast.json",
            params={"key": api_key, "q": location, "days": 3},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        current = data["current"]
        loc = data["location"]
        lines = [
            f"📍 {loc['name']}, {loc['country']}",
            f"🌡️ {current['temp_c']}°C — {current['condition']['text']}",
            f"💧 Humidity: {current['humidity']}%",
            "",
            "3-Day Forecast:",
        ]
        for day in data["forecast"]["forecastday"]:
            d = day["day"]
            lines.append(f"• {day['date']}: {d['condition']['text']} | High {d['maxtemp_c']}°C / Low {d['mintemp_c']}°C")
        return "\n".join(lines)
    except Exception as e:
        return f"Weather lookup failed: {e}"


@tool
def web_search_tool(query: str) -> str:
    """Search the web for travel info, attractions, visa requirements. Input: search query string."""
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return f"Web search not configured. Please search manually for: {query}"
    try:
        resp = requests.get(
            "https://serpapi.com/search",
            params={"q": query, "api_key": api_key, "num": 5},
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json().get("organic_results", [])
        if not results:
            return "No results found."
        lines = [f"Search results for: {query}\n"]
        for r in results[:4]:
            lines.append(f"• {r.get('title','')}: {r.get('snippet','')}")
        return "\n".join(lines)
    except Exception as e:
        return f"Search error: {e}"


@tool
def flight_search_tool(origin: str, destination: str, date: str) -> str:
    """Search for flights between two cities.
    
    Args:
        origin: Departure city name, e.g. 'Hyderabad'
        destination: Arrival city name, e.g. 'Mumbai'
        date: Travel date in YYYY-MM-DD format, e.g. '2025-08-15'
    """
    return (
        f"✈️ Sample Flights: {origin} → {destination} on {date}\n\n"
        "• AI Airways AA101 | Departs 06:30 → Arrives 09:45 | Economy ₹4,200\n"
        "• Sky Connect SC202 | Departs 10:15 → Arrives 13:30 | Economy ₹3,800\n"
        "• Global Air GA303 | Departs 14:00 → Arrives 17:20 | Economy ₹5,100\n\n"
        "Note: Set AVIATIONSTACK_KEY in .env for live flight data."
    )


@tool
def itinerary_tool(city: str, days: str) -> str:
    """Generate a day-by-day travel itinerary for a city.
    
    Args:
        city: Destination city name, e.g. 'Tokyo'
        days: Number of days as a string, e.g. '3'
    """
    try:
        num_days = int(days)
    except (ValueError, TypeError):
        num_days = 3

    plans = {
        "Tokyo": [
            "Shinjuku, Meiji Shrine, Harajuku",
            "Asakusa & Senso-ji Temple, Akihabara",
            "Shibuya crossing, teamLab, Roppongi",
            "Day trip to Mt. Fuji or Nikko",
            "Ginza shopping, Tsukiji market",
        ],
        "Paris": [
            "Eiffel Tower, Champ de Mars, Seine cruise",
            "Louvre Museum, Tuileries, Champs-Élysées",
            "Montmartre, Sacré-Cœur, Le Marais",
            "Versailles day trip",
            "Musée d'Orsay, Saint-Germain-des-Prés",
        ],
        "Hyderabad": [
            "Charminar, Laad Bazaar, Mecca Masjid",
            "Golconda Fort, Qutb Shahi Tombs",
            "Hussain Sagar, Lumbini Park, Birla Mandir",
            "Ramoji Film City",
            "Salar Jung Museum, Nehru Zoological Park",
        ],
        "Goa": [
            "Baga Beach, water sports, Calangute Beach",
            "Old Goa churches, Dudhsagar Waterfalls",
            "Palolem Beach, sunset cruise, night market",
            "Anjuna flea market, Vagator Beach",
            "Fort Aguada, spice plantation tour",
        ],
        "Dubai": [
            "Burj Khalifa, Dubai Mall, Dubai Fountain",
            "Desert Safari, dune bashing, BBQ dinner",
            "Palm Jumeirah, Atlantis, JBR Beach",
            "Gold Souk, Spice Souk, Dubai Creek",
            "Miracle Garden, Global Village",
        ],
        "Singapore": [
            "Marina Bay Sands, Gardens by the Bay, Merlion",
            "Sentosa Island, Universal Studios",
            "Chinatown, Little India, Clarke Quay",
            "Singapore Zoo, Night Safari",
            "Orchard Road shopping, hawker centres",
        ],
    }

    city_plan = plans.get(city, [f"Explore local attractions, museums, and cuisine of {city}"] * 5)
    lines = [f"🗺️ {num_days}-Day Itinerary for {city}\n"]
    for i in range(min(num_days, 5)):
        lines.append(f"Day {i+1}: {city_plan[i]}")
    if num_days > 5:
        for i in range(5, num_days):
            lines.append(f"Day {i+1}: Explore more of {city} at your own pace")
    return "\n".join(lines)