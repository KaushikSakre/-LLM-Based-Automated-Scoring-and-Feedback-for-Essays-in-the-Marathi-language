# results.py
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from context import Rubric

def generate_results(api_key, model_name, system_prompt, essay, temperature = 0.3):
    # Configure the LLM
    llm = ChatGroq(api_key=api_key, model_name=model_name, temperature = temperature)
    promptchat = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{essay}"),
        ]
    )
    chain = promptchat|llm
    results = chain.invoke({"Rubric":Rubric,"essay": essay})
  #score = float(results.content)
  #score = score
    return results.content
