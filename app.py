from flask import Flask, render_template, request, redirect, url_for, session
import random
from datetime import datetime
from dotenv import load_dotenv
import os

from gpt_utils import generate_gpt_question

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "mysecretkey")

QUESTIONS = {
    "smart": ["Что такое квантовая запутанность?"],
    "weird": ["Что бы ты сделал, если бы оказался на Марсе?"],
    "intimate": ["Что тебя больше всего ранило в любви?"],
    "action": ["Сделай другому участнику комплимент"]
}

CATEGORY_NAMES = {
    "smart": "♣️ Умное",
    "weird": "♦️ Странное",
    "intimate": "♥️ Интимное",
    "action": "♠️ Действие"
}

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/menu')
def menu():
    return render_template('index.html', category_names=CATEGORY_NAMES)

@app.route("/category/<category>")
def category(category):
    if category not in QUESTIONS:
        return render_template("chat.html", error="Категория не найдена.")

    question = random.choice(QUESTIONS[category])
    return render_template('chat.html',
                           question=question,
                           category=category,
                           category_names=CATEGORY_NAMES)

@app.route('/random_card')
def random_card():
    category = random.choice(list(QUESTIONS.keys()))
    question = random.choice(QUESTIONS[category])
    return render_template('chat.html',
                           question=question,
                           category=category,
                           category_names=CATEGORY_NAMES)

@app.route('/admin')
def admin():
    return render_template('admin.html', categories=CATEGORY_NAMES)

@app.route('/admin/add_question', methods=['POST'])
def add_question():
    category = request.form.get('category')
    question = request.form.get('question')

    if category in QUESTIONS and question:
        QUESTIONS[category].append(question.strip())
    return redirect(url_for('admin'))

@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    session['chat_history'] = []
    session.modified = True
    return redirect(url_for('index'))

@app.route('/start/<category>')
def start(category):
    if category not in QUESTIONS:
        return redirect(url_for('index'))

    if 'chat_history' not in session:
        session['chat_history'] = []

    # Добавляем выбор категории в историю
    session['chat_history'].append({
        'type': 'user',
        'message': CATEGORY_NAMES[category],
        'timestamp': datetime.now().strftime('%H:%M')
    })

    # Пробуем получить вопрос от GPT
    gpt_question = generate_ gpt_question(CATEGORY_NAMES[category])
    
    if gpt_question:
        question = gpt_question
    else:
        question = random.choice(QUESTIONS[category])

    # Добавляем вопрос от бота
    session['chat_history'].append({
        'type': 'bot',
        'message': f"📝 {question}",
        'timestamp': datetime.now().strftime('%H:%M')
    })

    session.modified = True
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)