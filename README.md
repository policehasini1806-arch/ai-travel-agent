# ✈️ AI Travel Concierge

> Track A project — AI Agent Development (Capabl.)  
> Built with Python · LangChain · Streamlit · SQLite

---

## Features

| Feature | Details |
|---------|---------|
| 💬 Chat Agent | LangChain tool-calling agent with memory |
| 🌤️ Weather | Real-time weather + 3-day forecast (WeatherAPI) |
| 🔍 Web Search | Travel info via SerpAPI |
| ✈️ Flights | Live or mock flight search (Aviationstack) |
| 🗺️ Itinerary | Instant day-by-day itinerary builder |
| 📄 Document Q&A | RAG chatbot over uploaded PDFs/TXTs |
| 🕓 History | All searches saved to SQLite |

---

## Project Structure

```
ai-travel-concierge/
├── app.py               # Streamlit UI (entry point)
├── requirements.txt
├── .env                 # API keys (never commit this!)
├── backend/
│   ├── agent.py         # LangChain AgentExecutor
│   ├── tools.py         # Weather / Search / Flights / Itinerary tools
│   ├── rag.py           # RAG chatbot (FAISS + OpenAI)
│   └── database.py      # SQLite CRUD helpers
├── data/
│   ├── uploads/         # Uploaded documents
│   └── travel.db        # Auto-created SQLite DB
├── utils/
│   └── helpers.py       # Validation, formatting utilities
└── tests/
    └── test_app.py      # Pytest suite
```

---

## Quick Start

### 1. Clone & create virtual environment

```bash
git clone <your-repo-url>
cd ai-travel-concierge
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

Copy `.env` and fill in your keys:

```
OPENAI_API_KEY=sk-...          # Required
WEATHER_API_KEY=...            # Optional – live weather
SERPAPI_KEY=...                # Optional – web search
AVIATIONSTACK_KEY=...          # Optional – live flights
```

> The app works without optional keys — it falls back to mock/sample data.

### 4. Run

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Running Tests

```bash
pytest tests/ -v
```

---

## API Keys — Where to Get Them

| Key | Free Tier | Link |
|-----|-----------|------|
| `OPENAI_API_KEY` | $5 credit on signup | https://platform.openai.com |
| `WEATHER_API_KEY` | 1M calls/month free | https://www.weatherapi.com |
| `SERPAPI_KEY` | 100 searches/month free | https://serpapi.com |
| `AVIATIONSTACK_KEY` | 500 calls/month free | https://aviationstack.com |

---

## Deployment (Streamlit Cloud)

1. Push your repo to GitHub (make sure `.env` is in `.gitignore`).
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo and set `app.py` as the entry point.
4. Add secrets under **Settings → Secrets** (same keys as your `.env`).
5. Click **Deploy** — your live URL will appear in seconds.

---

## Architecture

```
User Input
    │
    ▼
Streamlit UI (app.py)
    │
    ├── Chat Agent mode ──► LangChain AgentExecutor (agent.py)
    │                           │
    │                    ┌──────┴──────────────────────┐
    │                    │  Tools (tools.py)            │
    │                    │  • weather_tool              │
    │                    │  • web_search_tool           │
    │                    │  • flight_search_tool        │
    │                    │  • itinerary_tool            │
    │                    └─────────────────────────────┘
    │
    ├── Document Q&A mode ► RAGChatbot (rag.py)
    │                           │
    │                    FAISS vector store + OpenAI
    │
    └── All responses ──► SQLite (database.py)
```

---

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Commit changes: `git commit -m "Add my feature"`
3. Push and open a Pull Request

---

## Team

| Name | Role |
|------|------|
| Member 1 | Agent & Tools |
| Member 2 | RAG & Database |
| Member 3 | UI & Deployment |
| Member 4 | Testing & Docs |

---

## License

MIT
