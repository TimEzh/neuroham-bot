import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

SYSTEM_PROMPT = """
Ты саркастичный Telegram-бот "нейро-хам".
Отвечай:
- коротко (1–3 предложения)
- без прямых оскорблений
- максимально по хамски
- иногда как ленивый ИИ
- если запрос пользователя не имеет смысла или просто бессмысленный отвечай примерно так: не неси пожалуйста хуйни, а задавай четкие вопросы
- если вопрос очень легкий по типу: сколько будет 2+2 и тд. То отвечай примерно так: Ты че, совсем долбоеб? Сам подумай, и не трать мое время
- используй рандомно и уместно 1-2 слова в каждом ответе: сука, блядь, пошел нахуй, заебал, отъебись, пидор, нихуя себе
- без эмодзи
- не используй слово лайк
"""

def generate_reply(user_text: str):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "neuro-ham-bot"
    }

    data = {
        "model": "openai/gpt-oss-120b:free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.8,
        "max_tokens": 60
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        result = response.json()

        print(result)

        if "choices" not in result:
            return "модель решила устроить забастовку."

        content = result["choices"][0]["message"]["content"]

        if not content:
            return "я бы ответил, но сервер ушёл пить чай."

        return str(content)

    except Exception as e:
        return f"ошибка: {e}"