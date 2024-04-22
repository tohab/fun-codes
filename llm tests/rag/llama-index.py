from dotenv import load_dotenv
load_dotenv()

from llama_index.core import VectorStoreIndex,SimpleDirectoryReader,ServiceContext,PromptTemplate
from llama_index.llms import MistralAI
from llama_index.embeddings import MistralAIEmbedding
from llama_index import ServiceContext
# from llama_index.query_engine import RetrieverQueryEngine

import os

# Load data
reader = SimpleDirectoryReader(input_files=["essay.txt"])
documents = reader.load_data()

# Define LLM and embedding model
llm = MistralAI(api_key=os.getenv("OPENAI_API_KEY"), model="mistral-medium")
embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=os.getenv("MISTRAL_API_KEY"))
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

# Create vector store index
index = VectorStoreIndex.from_documents(documents, service_context=service_context)

# Create query engine
query_engine = index.as_query_engine(similarity_top_k=2)

def ask_llm(query):
    response = query_engine.query(query)
    return str(response)

# Take input from user, and store in variable "input"
user_question = input("Enter your question: ")
my_answer = ask_llm(user_question)
print(my_answer)