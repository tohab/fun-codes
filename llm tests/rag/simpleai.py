from dotenv import load_dotenv; load_dotenv()
import openai
import os
from simpleaichat import AIChat

client = openai.OpenAI(
    base_url = "https://api.endpoints.anyscale.com/v1",
    api_key = os.getenv("OPENAI_API_KEY")
)

AIChat(base_url = "https://api.endpoints.anyscale.com/v1", api_key=os.getenv("OPENAI_API_KEY"), system="you are an ai assistant")

AIChat()