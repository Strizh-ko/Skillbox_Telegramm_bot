from telebot.types import Message
from loader import bot
from database import history_commands


@bot.message_handler(commands=["history"])
def get_history(message: Message):
    history_commands.view(message.chat.id)