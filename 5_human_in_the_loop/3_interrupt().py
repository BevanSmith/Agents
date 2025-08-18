from langgraph.graph import START, END, StateGraph
from langgraph.types import Command, interrupt
from typing import TypedDict
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver


#this code focuses on interrupt which is better than user:

memory= MemorySaver()

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")



class State(TypedDict):
    value: str


def NodeA(state: State):
    print("NodeA")

    return Command(
        goto="NodeB",
        update={
            "value": state["text"] + "a"
        }
    )

def NodeB(state: State):
    print("NodeB")


    human_response = interrupt("Do you want to go to C or D?  Type C or D")

    print("human review: ", human_response)

    if human_response== "C":
        return Command(
            goto="NodeC",
            update={
                "value": state["value"] + "b"
            }
        )
    else:
        return Command(
            goto="NodeD",
            update={
                "value": state["value"] + "b"
            }
        )


def NodeC(state: State):
    print("NodeC")

    return Command(
        goto=END,
        update = {
            "value": state["value"] + "c"
        }
    )

def NodeD(state: State):
    print("NodeD")

    return Command(
        goto=END,
        update={
            "value":state["value"]+ "d"
        }
    )

graph = StateGraph(State)

graph.add_node("NodeA", NodeA)
graph.add_node("NodeB", NodeB)
graph.add_node("NodeC", NodeC)
graph.add_node("NodeD", NodeD)


graph.set_entry_point("NodeA")

app=graph.compile(checkpointer=memory)

config={"Configurable": {"thread_id":"1"}}

initialState={
    "value": ""
}


first_result=app.invoke(initialState, config, stream_mode="updates")

first_result