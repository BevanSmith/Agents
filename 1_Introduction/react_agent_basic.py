from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI()

result=llm.invoke("Give me a fact about dogs")

print(result)