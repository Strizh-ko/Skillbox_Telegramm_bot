from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.send_message(message.from_user.id, f"Приветствую! "
                                           f"Я - бот, который поможет вам подобрать отель в любой точке мира!\n"
                                           f"Нажмите 'Menu' бота и выберите одну из команд для поиска"
                                           f" в одном из режимов:\n"
                                           f"lowprice - самые дешевые\n"
                                           f"highprice - самые дорогие\n"
                                           f"bestdeal - лучшие в отношении цена/удаленность от центра")
