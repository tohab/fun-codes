import os
from dotenv import load_dotenv; load_dotenv()

import telebot
import requests

from dotenv import load_dotenv; load_dotenv()
import openai
import os

print(os.getenv("OPENAI_API_KEY"))

TOKEN = os.getenv("BOT_TOKEN")
print("BOT_TOKEN:", TOKEN)  # Add this line for debugging

bot = telebot.TeleBot(TOKEN)

# Command to greet the user
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy! How are you doing?")

# Command to get a joke from an API and send it to the user
@bot.message_handler(commands=['joke'])
def send_joke(message):
    joke_response = requests.get("https://api.chucknorris.io/jokes/random")
    if joke_response.status_code == 200:
        joke = joke_response.json()['value']
        bot.reply_to(message, joke)
    else:
        bot.reply_to(message, "Sorry, I couldn't fetch a joke at the moment. Try again later.")


# Command to query the language model
@bot.message_handler(commands=['llm'])
def query_llm(message):
    bot.reply_to(message, "Please enter your query:")
    bot.register_next_step_handler(message, process_query)

def process_query(message):
    query = message.text
    try:
        # Send query to OpenAI language model
        chat_completion = openai.Completion.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."}, 
                {"role": "user", "content": query}
            ],
            temperature=0.7
        )
        response = chat_completion.choices[0].message.content
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

# # Echo handler to respond to any text message
# @bot.message_handler(func=lambda msg: True)
# def echo_all(message):
#     bot.reply_to(message, "You said: " + message.text)

# Command to provide help and list available commands
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "I can do a few things:\n\n"
    help_text += "/hello - Say hello\n"
    help_text += "/joke - Tell a joke\n"
    help_text += "/llm - Get a response from Rohan's LLM model\n"
    help_text += "/help - Show this help message\n"

    bot.reply_to(message, help_text)

# Run the bot indefinitely
bot.infinity_polling()