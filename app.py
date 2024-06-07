from flask import Flask, render_template, request, session
import openai
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = os.getenv("SECRET_KEY")

# Initial questions
questions = [
    "Please provide your general information like (name, age, contact number, address).",
    "What is your academic performance? (Current Grade, Current Grade Point Avg, Current Stream, Current Curriculum)",
    "What is your goal in which area?"
]

@app.route('/')
def home():
    session.clear()
    session['question_index'] = 0
    return render_template('chat.html')

@app.route('/process_chat', methods=['POST'])
def process_chat():
    user_input = request.form.get('user_input')
    if user_input:
        question_index = session.get('question_index', 0)
        if question_index < len(questions):
            next_question = questions[question_index]
            session['question_index'] = question_index + 1
            return next_question
        else:
            bot_response = get_ai_response(user_input)
            return bot_response
    return "Invalid input"

def get_ai_response(input_text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_text}
        ]
    )
    return completion.choices[0].message['content']

if __name__ == '__main__':
    app.run(debug=True)
