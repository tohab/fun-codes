from dotenv import load_dotenv
load_dotenv()
import os
import langchain
import langchain_openai
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Set up OpenAI API client
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = langchain_openai.OpenAI(temperature=0, openai_api_key=openai_api_key)

# Load the directory of text files into a vector store
vector_store = FAISS.from_texts(
    [open(r"llm tests/essay.txt", encoding="utf-8").read()],
    langchain.llms.OpenAI(openai_api_key=openai_api_key, temperature=0),
    allow_dangerous_deserialization=True
)

# Create the Retrieval QA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    return_source_documents=True,
)

# Take input from user and generate response
user_query = input("Enter your query: ")
result = qa({"query": user_query})
print(result['result'])