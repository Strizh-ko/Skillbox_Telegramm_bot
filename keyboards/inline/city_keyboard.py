from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot
from project import RapidAPI


def city_buttons(cities: dict):
    print(cities)
    keyboard = InlineKeyboardMarkup()
    for city_name, city_id in cities.items():
        keyboard.add(InlineKeyboardButton(city_name, callback_data=city_id))
    return keyboard


