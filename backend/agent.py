import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from backend.tools import weather_tool, web_search_tool, flight_search_tool, itinerary_tool

SYSTEM_PROMPT = """You are an expert AI Travel Concierge. Help users plan trips, find flights, check weather, and build itineraries.

When using tools:
- weather_tool: pass only the city name as a string
- flight_search_tool: pass origin, destination, and date as separate arguments
- itinerary_tool: pass city as string and days as integer
- web_search_tool: pass a search query string

Always be concise and friendly. Present results as clear bullet lists."""


class TravelAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY not set in .env")

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key,
            temperature=0.3,
        )

        self.tools = [weather_tool, web_search_tool, flight_search_tool, itinerary_tool]

        self.agent = create_react_agent(
            model=self.llm,
            tools=self.tools,
            prompt=SYSTEM_PROMPT,
        )

        self.chat_history = []

    def run(self, user_input: str) -> str:
        try:
            self.chat_history.append(HumanMessage(content=user_input))
            result = self.agent.invoke({"messages": self.chat_history})
            output = result["messages"][-1].content
            self.chat_history.append(AIMessage(content=output))
            self.chat_history = self.chat_history[-20:]
            return output
        except Exception as exc:
            return f"⚠️ Agent error: {exc}"