from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_buttons():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Все верно", callback_data='Все верно'))
    return keyboard
