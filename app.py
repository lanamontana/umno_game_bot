import os
import random
import logging
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET",
                                "fallback_secret_key_for_development")

# Вопросы по категориям (в памяти сервера)
QUESTIONS = {
    "smart": [
        "Что бы ты изменил в своей жизни, если бы знал, что последствий не будет?",
        "Какая твоя самая большая мечта, которую ты никому не рассказывал?",
        "О чем ты думаешь перед сном?",
        "Какой урок жизни дался тебе труднее всего?",
        "Что значит для тебя быть счастливым?",
        "Если бы ты мог прожить один день в прошлом, какой бы это был день?",
        "Какая твоя самая большая слабость?",
        "Что ты больше всего ценишь в людях?",
        "Какой совет ты бы дал своему прошлому 'я'?",
        "Что заставляет тебя чувствовать себя живым?"
    ],
    "strange": [
        "Если бы ты был супергероем, какая была бы твоя самая бесполезная суперсила?",
        "Какой самый странный сон ты помнишь?",
        "Если бы животные могли говорить, с каким из них ты бы точно не хотел разговаривать?",
        "Какую самую странную еду ты когда-либо пробовал?",
        "Если бы ты мог быть любым предметом в доме, каким бы ты был?",
        "Какая самая странная привычка у тебя была в детстве?",
        "Если бы ты оказался в лифте с призраком, о чем бы вы поговорили?",
        "Какой самый странный комплимент ты когда-либо получал?",
        "Если бы ты мог изобрести новый праздник, какой бы это был праздник?",
        "Какое самое странное место, где ты засыпал?"
    ],
    "intimate": [
        "Какое самое романтичное место для свидания, о котором ты мечтаешь?",
        "Что для тебя означает близость в отношениях?",
        "Какой комплимент тебе больше всего нравится получать?",
        "Что делает тебя особенно привлекательным в глазах других?",
        "Какой твой язык любви?",
        "Что ты больше всего ценишь в романтических отношениях?",
        "Какое самое красивое признание в любви ты слышал?",
        "Что заставляет тебя чувствовать себя желанным?",
        "Какой момент в отношениях самый волнующий для тебя?",
        "Что для тебя идеальный вечер с любимым человеком?"
    ],
    "action": [
        "Покажи свой самый смешной танец",
        "Изобрази любое животное, а партнер должен угадать",
        "Расскажи анекдот или смешную историю",
        "Покажи, как ты выглядишь, когда сильно удивлен",
        "Изобрази известную личность", "Покажи свой талант (любой)",
        "Сделай комплимент партнеру, говоря только рифмами",
        "Покажи, как ты танцуешь под разную музыку",
        "Изобрази эмоцию, которую выберет партнер",
        "Покажи свое коронное селфи-лицо"
    ]
}

CATEGORY_NAMES = {
    "smart": "♣️ умное",
    "strange": "♦️ странное",
    "intimate": "♥️ интимное",
    "action": "♠️ действие"
}


@app.route('/')
def index():
    if 'chat_history' not in session:
        session['chat_history'] = []
    return render_template('index.html', chat_history=session['chat_history'])


@app.route('/start', methods=['POST'])
def start_game():
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Добавляем команду пользователя
    session['chat_history'].append({
        'type':
        'user',
        'message':
        '/start',
        'timestamp':
        datetime.now().strftime('%H:%M')
    })

    # Добавляем приветствие бота
    welcome_message = """Привет! 👋 Я бот для парной игры с вопросами!

Выберите категорию вопросов:

♣️ умное - глубокие и философские вопросы
♦️ странное - необычные и забавные вопросы  
♥️ интимное - романтические и личные вопросы
♠️ действие - задания для выполнения

Нажмите на кнопку с нужной категорией!"""

    session['chat_history'].append({
        'type':
        'bot',
        'message':
        welcome_message,
        'timestamp':
        datetime.now().strftime('%H:%M')
    })

    session.modified = True
    return redirect(url_for('index'))


@app.route('/question/<category>', methods=['POST'])
def get_question(category):
    if 'chat_history' not in session:
        session['chat_history'] = []

    if category not in QUESTIONS:
        return redirect(url_for('index'))

    # Добавляем выбор категории пользователем
    session['chat_history'].append({
        'type':
        'user',
        'message':
        CATEGORY_NAMES[category],
        'timestamp':
        datetime.now().strftime('%H:%M')
    })

    # Выбираем случайный вопрос
    question = random.choice(QUESTIONS[category])

    # Добавляем вопрос от бота
    session['chat_history'].append({
        'type':
        'bot',
        'message':
        f"📝 {question}",
        'timestamp':
        datetime.now().strftime('%H:%M')
    })

    session.modified = True
    return redirect(url_for('index'))


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

    return redirect(url_for('admin'))


@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    session['chat_history'] = []
    session.modified = True
    return redirect(url_for('index'))


@app.route("/category/<category>")
def category(category):
    if category in QUESTIONS:
        question = random.choice(QUESTIONS[category])
        return render_template('chat.html',
                               question=question,
                               category=category,
                               category_names=CATEGORY_NAMES)
    else:
        return render_template("chat.html", error="Категория не найдена.")


@app.route('/')
def intro():
    return render_template('intro.html')


@app.route('/menu')
def menu():
    return render_template('index.html', category_names=CATEGORY_NAMES)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


@app.route('/random_card')
def random_card():
    import random
    category = random.choice(list(QUESTIONS.keys()))
    question = random.choice(QUESTIONS[category])
    return render_template('chat.html',
                           question=question,
                           category=category,
                           category_names=CATEGORY_NAMES)
