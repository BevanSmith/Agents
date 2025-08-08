from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langchain_tavily import TavilySearch
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class BasicChatBot(TypedDict):
    messages: Annotated[list,add_messages]

search_tool = TavilySearch(max_results=2)
tools=[search_tool]

llm=ChatGroq(model="llama-3.1-8b-instant")
llm_with_tools=llm.bind_tools(tools=tools)

result=llm_with_tools.invoke("Hi, whats the weather in new york")

print(result)