import llama_index.core as llama
# from llama_index.agent import ReActAgent
from dotenv import load_dotenv; load_dotenv()
import openai
import os

client = openai.OpenAI(
    base_url = "https://api.endpoints.anyscale.com/v1",
    api_key = os.getenv("OPENAI_API_KEY")
)


documents = llama.SimpleDirectoryReader(r"data/rohan.txt").load_data()

# Define an LLM
llm = client.chat.completions.create(model="gpt-4")

# Build index with a chunk_size of 512
node_parser = llama.SimpleNodeParser.from_defaults(chunk_size=512)
nodes = node_parser.get_nodes_from_documents(documents)
vector_index = llama.VectorStoreIndex(nodes)

query_engine = vector_index.as_query_engine()

response_vector = query_engine.query("What did the author do growing up?")

response_vector.response