from dotenv import load_dotenv; load_dotenv()
import openai
import os

client = openai.OpenAI(
    base_url = "https://api.endpoints.anyscale.com/v1",
    api_key = os.getenv("OPENAI_API_KEY")
)

def ask_llm(query):
    chat_completion = client.chat.completions.create(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, 
            {"role": "user", "content": query}],
        temperature=0.7
    )
    return chat_completion.choices[0].message.content


# Take input from user, and store in variable "input"
user_question = input("Enter your question: ")
my_answer = ask_llm(user_question)

print(my_answer)