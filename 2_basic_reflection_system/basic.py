from typing import List, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from chains import generation_chain, reflection_chain

load_dotenv()

class AgentState(TypedDict):
    messages: List[BaseMessage]


graph=StateGraph(AgentState)

def generate_node(state: AgentState):
    return {"messages": state["messages"] + [generation_chain.invoke(state)]}

def reflect_node(state: AgentState):
    return {"messages": state["messages"] + [reflection_chain.invoke(state)]}



graph.add_node("generate_node", generate_node)
graph.add_node("reflect_node", reflect_node)


graph.set_entry_point("generate_node")

def should_continue(state: AgentState):
    if(len(state["messages"]) > 4):
        return END
    return "reflect_node"



graph.add_conditional_edges("generate_node", should_continue, {"reflect_node": "reflect_node", END: END})
graph.add_edge("reflect_node", "generate_node")


app = graph.compile()

#to plot graph
print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()


response = app.invoke({"messages": [HumanMessage(content="AI Agent taking over content creation")]},
                      {"recursion_limit": 20})

print(response)