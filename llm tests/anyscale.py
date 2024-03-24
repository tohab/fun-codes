from dotenv import load_dotenv; load_dotenv()
import openai
import os

client = openai.OpenAI(
    base_url = "https://api.endpoints.anyscale.com/v1",
    api_key = os.getenv("OPENAI_API_KEY")
)

# Take input from user, and store in variable "input"
query = input("Enter your query: ")


# Note: not all arguments are currently supported and will be ignored by the backend.
chat_completion = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[{"role": "system", "content": "You are a helpful assistant."}, 
              {"role": "user", "content": query}],
    temperature=0.7
)

response = chat_completion.choices[0].message.content

print(response)