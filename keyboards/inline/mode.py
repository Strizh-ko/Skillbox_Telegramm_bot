from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def mode_buttons():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Пока не знаю", callback_data='Пока не знаю'))
    return keyboard