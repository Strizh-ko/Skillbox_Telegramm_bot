from telebot.types import Message
from utils import date
import project.RapidAPI
from states.st_find_hotel import FindHotelState
from loader import bot
from project import RapidAPI
from keyboards import inline


@bot.message_handler(commands=["lowprice", 'highprice', 'bestdeal'])
def get_location(message: Message):
    bot.reply_to(message, f"Хорошо, введите город назначения")
    bot.set_state(message.from_user.id, FindHotelState.location, message.chat.id)


@bot.message_handler(state=FindHotelState.location)
def get_target_location(message: Message):

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['cities_dct'] = RapidAPI.location(message.text)

        if len(data['cities_dct']) > 1:
            bot.send_message(message.from_user.id,
                             "Уточните, пожалуйста город",
                             reply_markup=inline.city_keyboard.city_buttons(data['cities_dct']))
            bot.set_state(message.from_user.id, FindHotelState.date, message.chat.id)

        elif len(data['cities_dct']) == 1:

            bot.send_message(message.chat.id, "Введите дату своего прибытия в формате ДД.ММ.ГГ")
            bot.set_state(message.from_user.id, FindHotelState.date, message.chat.id)

        else:
            bot.send_message(message.from_user.id,
                             "Название города введено не корректно. Пожалуйста, повторите попытку")


@bot.message_handler(state=FindHotelState.date)
def get_date(message: Message):
    if date.arrivedate(message.text):
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['ad'], data['am'], data['ay'], data['o'] = date.arrivedate(message.text)

        bot.send_message(message.from_user.id, f"Принято.\nНа сколько дней?")
        bot.set_state(message.from_user.id, FindHotelState.days, message.chat.id)
    else:
        bot.send_message(message.from_user.id, f"Введена не корректная дата. Пожалуйста повторите попытку.")


@bot.message_handler(state=FindHotelState.days)
def get_days(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if date.departdate(message.text, data['o']):
            data['dd'], data['dm'], data['dy'] = date.departdate(message.text, data['o'])

            bot.send_message(message.from_user.id, f"Ок, Записал.\n"
                                                   f"Сколько будет человек?")
            bot.set_state(message.from_user.id, FindHotelState.people, message.chat.id)
        else:
            bot.send_message(message.from_user.id, f"Количество дней пребывания должно быть натуральным числом.\n"
                                                   f"Пожалуйста повторите попытку.")


@bot.message_handler(state=FindHotelState.people)
def get_people(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['people'] = int(message.text)

            bot.send_message(message.from_user.id,
                             f"Понял, принял.\n"
                             f"Перед тем как начать подбор, давайте подтвердим информацию...\n\n"
                             f"Город назначения: {list(data['cities_dct'].items())[0][0]}\n"
                             f"Дата прибытия: {data['ad']}.{data['am']}.{data['ay']}\n"
                             f"Дата отбытия: {data['dd']}.{data['dm']}.{data['dy']}\n"
                             f"Количество человек: {data['people']}\n\n"
                             f"Все верно?",
                             reply_markup=inline.confirm.confirm_buttons()
                             )
        bot.set_state(message.from_user.id, FindHotelState.mode, message.chat.id)

    else:
        bot.send_message(message.from_user.id, f"Количество прибывающих человек должно быть натуральным числом. "
                                               f"Давайте еще разок. Сколько вас?")

