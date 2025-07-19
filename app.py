import os
import openai
import telebot
from dotenv import load_dotenv
from datetime import datetime
import random

# Загрузка переменных из .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

# Папка для сохранения вопросов
QUESTIONS_DIR = "questions"
os.makedirs(QUESTIONS_DIR, exist_ok=True)

# Словарь с категориями
CATEGORIES = {
    "♣️ умное": "smart",
    "♦️ странное": "weird",
    "♥️ интимное": "intimate",
    "♠️ действие": "action"
}

# Генерация вопроса с GPT
def generate_question(category):
    try:
        prompt_map = {
            "smart": "Придумай глубокий философский вопрос для парной игры.",
            "weird": "Придумай странный, забавный вопрос для парной игры.",
            "intimate": "Придумай интимный, романтический вопрос для парной игры.",
            "action": "Придумай задание для двоих игроков в парной игре."
        }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_map[category]}],
            max_tokens=60,
            temperature=0.8,
        )

        question = response.choices[0].message["content"].strip()

        # Сохраняем в файл
        file_path = os.path.join(QUESTIONS_DIR, f"{category}.txt")
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(question + "\n")

        return question

    except Exception as e:
        print(f"Ошибка GPT: {e}")
        return load_saved_question(category)

# Если GPT не работает — подгружаем сохранённый вопрос
def load_saved_question(category):
    file_path = os.path.join(QUESTIONS_DIR, f"{category}.txt")
    if not os.path.exists(file_path):
        return "Нет вопросов в базе 🫣"
    with open(file_path, "r", encoding="utf-8") as f:
        questions = [q.strip() for q in f if q.strip()]
    return random.choice(questions) if questions else "Вопросы закончились!"

# Команды Telegram-бота
@bot.message_handler(commands=["start"])
def start_game(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for label in CATEGORIES:
        markup.add(label)
    bot.send_message(message.chat.id, "Выбери категорию вопроса:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in CATEGORIES)
def ask_question(message):
    category_key = message.text
    category_code = CATEGORIES[category_key]
    question = generate_question(category_code)
    bot.send_message(message.chat.id, f"🃏 {question}")

# Запуск
if __name__ == "__main__":
    bot.infinity_polling()

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
