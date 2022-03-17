import telebot

from config import TOKEN
from main import Functions


bot = telebot.TeleBot(TOKEN)
model = Functions()

@bot.message_handler(commands=['start'])
def begin(message):
    user_name = message.from_user.first_name
    client_id = message.from_user.id
    bot.send_message(
        chat_id = client_id,
        text = f'Hello, {user_name}!\nI can help you to translate a text from Georgian-Latin to Russian'
        )

@bot.message_handler(content_types=['text'])
def text_handler(message):
    client_id = message.from_user.id
    user_message = message.text

    text, link = model.pipeline(user_message)
    bot.send_message(
        chat_id = client_id,
        text = text
    )
    bot.send_message(
        chat_id = client_id,
        parse_mode='Markdown',
        text = f'[Google Translate link]({link})'
    )

if __name__ == '__main__':
    bot.polling(none_stop=True)
