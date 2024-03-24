from langchain.document_loaders import TextLoader
from langchain.llms import OpenAIChat
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma

import openai
import os

# Custom OpenAI client for Anyscale
client = openai.OpenAI(
    base_url = "https://api.endpoints.anyscale.com/v1",
    api_key = os.getenv("OPENAI_API_KEY")
)

# Update the loader to use TextLoader and point to your .txt file
loader = TextLoader("C:/Users/malat/Desktop/fun codes/llm tests/test-post.txt")
docs = loader.load_and_split()

embeddings = OpenAIEmbeddings()

chroma_db = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="data",
    collection_name="lc_chroma_demo"
)

query = "What is this document about?"

# Custom LLM using the Anyscale client
llm = OpenAIChat(
    openai_api=client,
    model_name="mistralai/Mixtral-8x7B-Instruct-v0.1",
    temperature=0.7
)

chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=chroma_db.as_retriever())

response = chain(query)
