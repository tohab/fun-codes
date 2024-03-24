from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai
import os
import markdown

app = Flask(__name__)
load_dotenv()

client = openai.OpenAI(
    base_url="https://api.endpoints.anyscale.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        chat_completion = client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": query}],
            temperature=0.7
        )
        response = chat_completion.choices[0].message.content
        html_response = markdown.markdown(response)
        return render_template(os.path.join('templates', 'index.html'), response=html_response)
    return render_template(os.path.join('templates', 'index.html'))

if __name__ == '__main__':
    app.run(debug=True)