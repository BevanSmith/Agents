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

def chatbot(state:BasicChatBot):
    return {
        "messages": [llm_with_tools.invoke(state["messages"])] #note that the entire state["messages"] is fed in here
        # in contrast to only "messages" fed into app.invoke.  that is because app.invoke takes in a first message
        # but here it uses the entire message history
    }


def tools_router(state:BasicChatBot):
    last_message=state["messages"][-1]  #getting the last AI message
# last_message is an AI object and if a tool is called, it creates a specific entry called "tool_calls"
# so this node checks if it exists and if it is actually populated.
    if (hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):
        return "tool_node"
    else:
        return END

tool_node = ToolNode(tools=tools)  #looks at messages


graph=StateGraph(BasicChatBot)

graph.add_node("chatbot", chatbot)
graph.add_node("tool_node", tool_node)

graph.set_entry_point("chatbot")
graph.add_conditional_edges("chatbot",tools_router)
graph.add_edge("tool_node", "chatbot")


app=graph.compile()


# while true allows for infinite looping until exit or end and break.
# the user (human) inputs a prompt, if not exit or end, it goes to
# invoke the app with the human message.  The app produces some llm output and
# stores in result which we then print to screen, and go back to User
#This loops until we break. 
while True:
    user_input = input("User: ")
    if(user_input in ["exit", "end"]):
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        })   #the app is designed to accept input as a dictionary with a key and value

        # print("Bot:", result["messages"][-1].content)
        print(result)
















        