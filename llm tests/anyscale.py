from dotenv import load_dotenv; load_dotenv()
import openai
import os

client = openai.OpenAI(
    base_url = "https://api.endpoints.anyscale.com/v1",
    api_key = os.getenv("OPENAI_API_KEY")
)

def ask_llm(query):
    chat_completion = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, 
            {"role": "user", "content": query}],
        temperature=1.0
    )
    return chat_completion.choices[0].message.content

# Loop to prompt user for one-off queries
while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = ask_llm(prompt)
    print(result)
    

# Anyscale supports the following models.
#     meta-llama/Llama-3-8b-chat-hf
#     meta-llama/Llama-3-70b-chat-hf
#     meta-llama/Llama-2-7b-chat-hf
#     meta-llama/Llama-2-13b-chat-hf
#     meta-llama/Llama-2-70b-chat-hf
#     codellama/CodeLlama-70b-Instruct-hf
#     mistralai/Mistral-7B-Instruct-v0.1
#     mistralai/Mixtral-8x7B-Instruct-v0.1
#     mistralai/Mixtral-8x22B-Instruct-v0.1