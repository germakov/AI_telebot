import logging

import telebot

from openai import OpenAI

from config import CHATGPT_TOKEN, TG_BOT_TOKEN

logger = logging.getLogger("TeleBot")

formatter = logging.Formatter(
    '%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"'
)

# Настройка API ключа OpenAI
API_KEY_OPENAI = CHATGPT_TOKEN
BASE_URL_OPENAI = "https://openai.javarush.com/v1"
# BASE_URL_OPENAI = "https://api.proxyapi.ru/openai/v1/"

# Настройка API ключа Telegram
API_KEY_TELEGRAM = TG_BOT_TOKEN

# Создание клиента OpenAI
client = OpenAI(
    api_key=API_KEY_OPENAI,
    base_url=BASE_URL_OPENAI,
)

# Создание клиента Telegram
bot = telebot.TeleBot(API_KEY_TELEGRAM)


def send_message_to_openai(message):
    """Отправляет сообщение в нейросеть OpenAI"""
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}]
    )

    return chat_completion.choices[0].message.content


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Добро пожаловать в чат с нейросетью! Отправьте мне сообщение, и я отвечу.",
    )


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    user_input = message.text
    response = send_message_to_openai(user_input)
    bot.reply_to(message, response)


# Запуск бота
if __name__ == "__main__":
    print("Бот запущен и ожидает сообщений...")
    # bot.polling(none_stop=True)
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=10)
        except Exception as e:
            print(e)
