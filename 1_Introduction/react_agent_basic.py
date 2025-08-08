from langchain_groq import ChatGroq # Updated to ChatGroq
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from langchain.agents import initialize_agent, AgentExecutor, create_react_agent, tool
from langchain_community.tools import TavilySearchResults
from langchain_core.prompts import PromptTemplate
import datetime


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama-3.1-8b-instant", temperature=0.0)

search_tool = TavilySearchResults(search_depth="basic")

@tool
def get_system_time(format: str="%Y-%m-%d %H:%M:%S"):
    """Returns the current data and time in the specified format"""

    current_time=datetime.datetime.now()
    formatted_time=current_time.strftime(format)
    return formatted_time
    

tools=[search_tool, get_system_time]
# Get the ReAct prompt from the LangChain hub
# This is a pre-built, robust prompt that includes the Final Answer instructions
base_prompt = hub.pull("hwchase17/react")


agent=initialize_agent(tools=tools,llm=llm,agent="zero-shot-react-description",verbose=True)


agent.invoke("When was the rugby world cup final and how long ago was it")



# result=llm.invoke("Give me a tweet about today's weather in Johannesburg")

# print(result.content)