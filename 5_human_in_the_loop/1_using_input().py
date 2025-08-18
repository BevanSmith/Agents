from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatGroq(model="llama-3.1-8b-instant")

GENERATE_POST = "generate_post"
GET_REVIEW_DECISION = "get_review_decision"
POST = "post"
COLLECT_FEEDBACK = "collect_feedback"


def generate_post(state: State):
    return {
        "messages": [llm.invoke(state["messages"])]  #why is this fed the entire state.messages and not
        #the user input human message?
    }

def get_review_decision(state: State):
    post_content = state["messages"][-1].content   #extracts last message

    print("\n Current LinkedIn Post: \n")
    print(post_content)
    print("\n")

    decision=input("Post to LinkedIn?  yes/no: ")

    if decision.lower() == "yes":
        return POST
    else:
        return COLLECT_FEEDBACK
    

def post(state: State):
    final_post = state["messages"][-1].content
    print("\n Final Post: \n")
    print(final_post)
    print("\n Post has been approved and is now live on LinkedIn!")


def collect_feedback(state: State):
    feedback = input("How can I improve this post?")
    return{
        "messages": [HumanMessage(content=feedback)]  #this is not feeding into llm but storing in humanmessage. to be
        #fed back to generate post which receives the state.human message and
    }

graph = StateGraph(State)

graph.add_node(GENERATE_POST, generate_post)
graph.add_node(GET_REVIEW_DECISION, get_review_decision)
graph.add_node(COLLECT_FEEDBACK, collect_feedback)
graph.add_node(POST,post)


graph.set_entry_point(GENERATE_POST)

graph.add_conditional_edges(GENERATE_POST, get_review_decision)
graph.add_edge(POST, END)
graph.add_edge(COLLECT_FEEDBACK, GENERATE_POST)


app=graph.compile()

response = app.invoke({
    "messages": [HumanMessage(content="write a short poem about the lonely life of an AI.")]
})

print(response)