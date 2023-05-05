from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def city_buttons(cities: dict):
    keyboard = InlineKeyboardMarkup()
    for city_name, city_id in cities.items():
        keyboard.add(InlineKeyboardButton(city_name, callback_data=city_id))
    return keyboard


