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


## Team

| Name |
|------|
|M.Aasritha| 
|D.Meghana|
|P.Hasini|
|Sevitha|

---

## License

MIT
