from langgraph.graph import START, END, StateGraph
from langgraph.types import Command
from typing import TypedDict
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv


#this code shows how to use Command within a node, instead of using add_edges.  It's meant to provide
#more flexibility.  But not sure exaclty how yet.  The Command class can show which node to goto
#and it can update the state


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class State(TypedDict):
    text: str


def NodeA(state: State):
    print("NodeA")

    return Command(
        goto="NodeB",
        update={
            "text": state["text"] + "a"
        }
    )

def NodeB(state: State):
    print("NodeB")

    return Command(
        goto="NodeC",
        update={
            "text":state["text"] + "b"
        }
    )

def NodeC(state: State):
    print("NodeC")

    return Command(
        goto=END,
        update = {
            "text": state["text"] + "c"
        }
    )

graph = StateGraph(State)

graph.add_node("NodeA", NodeA)
graph.add_node("NodeB", NodeB)
graph.add_node("NodeC", NodeC)


graph.set_entry_point("NodeA")

app=graph.compile()

response= app.invoke({
    "text": ""
})

response