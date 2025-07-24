print("🧪 Старт теста")

try:
    from gpt_utils import generate_gpt_question  # если ты именно так её назвала

    question = generate_gpt_question("intimate")
    print("✅ GPT вопрос:", question)

except Exception as e:
    print("❌ Ошибка:", e)