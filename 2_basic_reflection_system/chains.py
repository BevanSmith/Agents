from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

generation_prompt=ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a twitter technie influence assistant tasked with writing twitter posts."
         "Generate the best twitter (X) post possible for the user's request."
         "If the use provides critique, respond with a revised version of your previous attempts.",
         ),
         MessagesPlaceholder(variable_name="messages"),
    ]
)


reflection_prompt=ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a viral twitter influence grading a tweet."
         "Generate critique and recommendations for the user's tweet."
         "Always provide detailed recommendations, including requests for length, viratlity adn style, etc..",
         ),
         MessagesPlaceholder(variable_name="messages"),
    ]
)

llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash")

generation_chain=generation_prompt | llm
reflection_chain=reflection_prompt | llm

