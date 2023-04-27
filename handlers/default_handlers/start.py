from telebot.types import Message

from loader import bot



@bot.message_handler(commands=["start"])
def bot_start(message: Message):

    bot.send_message(message.from_user.id, f"Приветствую! Я - бот, который поможет вам подобрать отель в любой точке мира!")
