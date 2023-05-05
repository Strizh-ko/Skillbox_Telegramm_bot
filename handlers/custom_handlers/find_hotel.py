from telebot.types import Message, InputMediaPhoto
from utils import date, hotel_filter, RapidAPI
from states.st_find_hotel import FindHotelState
from loader import bot
from keyboards import inline
from database import history_commands


@bot.message_handler(commands=["lowprice", 'highprice', 'bestdeal'])
def get_location(message: Message):
    bot.reply_to(message, f"Хорошо, введите город назначения")
    bot.set_state(message.from_user.id, FindHotelState.location, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text


@bot.message_handler(state=FindHotelState.location)
def get_target_location(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['cities_dct'] = RapidAPI.location(message.text)

        if len(data['cities_dct']) > 1:
            bot.send_message(message.from_user.id,
                             "Уточните, пожалуйста город",
                             reply_markup=inline.city_keyboard.city_buttons(data['cities_dct']))

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
            data['search_param_text'] = f"Город назначения: {list(data['cities_dct'].items())[0][0]}\n" \
                                        f"Дата прибытия: {data['ad']}.{data['am']}.{data['ay']}\n" \
                                        f"Дата отбытия: {data['dd']}.{data['dm']}.{data['dy']}\n" \
                                        f"Количество человек: {data['people']}\n"
            if data['command'] == '/bestdeal':
                bot.send_message(message.from_user.id, f'Далее, на какую максимальную стоимость вы раcчитываете?')
                bot.set_state(message.from_user.id, FindHotelState.price, message.chat.id)

            else:
                bot.send_message(message.from_user.id, f"Понял, принял.\n"
                                                       f"Перед тем как начать подбор, "
                                                       f"давайте подтвердим информацию...\n\n"
                                                       f"{data['search_param_text']}\n"
                                 f"Все верно? Если хотите что-то поправить, просто выберите новую команду через меню.",
                                 reply_markup=inline.confirm.confirm_buttons()
                                 )
                bot.set_state(message.from_user.id, FindHotelState.quantity, message.chat.id)

    else:
        bot.send_message(message.from_user.id, f"Количество прибывающих человек должно быть натуральным числом. "
                                               f"Давайте еще разок. Сколько вас?")


@bot.message_handler(state=FindHotelState.price)
def get_price(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['price'] = int(message.text)
        bot.send_message(message.from_user.id, f"И последнее... Желаемая максимальная дистанция от центра? (в метрах)")
        bot.set_state(message.from_user.id, FindHotelState.distance, message.chat.id)
    else:
        bot.send_message(message.from_user.id, f"Максимальная стоимость должна быть натуральным числом. "
                                               f"Давайте еще разок.")


@bot.message_handler(state=FindHotelState.distance)
def get_distance(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance'] = int(message.text) / 1000
            data['search_param_text'] += f"Максимальная цена: {data['price']}\n" \
                                         f"Удаленность от центра: {data['distance']} км.\n"
            bot.send_message(message.from_user.id,
                             f"Понял, принял.\n"
                             f"Перед тем как начать подбор, давайте подтвердим информацию...\n\n"
                             f"{data['search_param_text']}\n"
                             f"Все верно? Если хотите что-то поправить, просто выберите новую команду через меню.",
                             reply_markup=inline.confirm.confirm_buttons())
        bot.set_state(message.from_user.id, FindHotelState.quantity, message.chat.id)
    else:
        bot.send_message(message.from_user.id, f"Максимальная стоимость должна быть натуральным числом. "
                                               f"Давайте еще разок.")


@bot.message_handler(state=FindHotelState.quantity)
def get_quantity(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit() and 0 < int(message.text) <= len(data['hotels_lst']):
            if data['command'] == '/bestdeal':
                selected_hotels = hotel_filter.bd_filter(data['hotels_lst'], int(message.text),
                                                         data['price'], data['distance'])
            else:
                selected_hotels = hotel_filter.filter(data['command'], data['hotels_lst'], int(message.text))
            bot.send_message(message.from_user.id, 'Выбираю для вас лучшие отели... Ожидайте.\n')
            data['hotel_detail'] = RapidAPI.hotels_detail(selected_hotels)
            bot.send_message(message.from_user.id, 'Хотите посмотреть фото отелей?')
            bot.set_state(message.from_user.id, FindHotelState.photo, message.chat.id)
        else:
            bot.send_message(message.from_user.id, f"Не корректно введено число желаемых для просмотра отелей.\n"
                                                   f"Введите натуральное число не больше {len(data['hotels_lst'])}")



@bot.message_handler(state=FindHotelState.photo)
def get_photo(message: Message):
    if message.text.lower() in ['да', 'yes', 'конечно', 'угу', 'ага', '+', 'давай']:
        bot.send_message(message.from_user.id, 'Могу показать до 10ти фото каждого отеля. Сколько хотите?')
        bot.set_state(message.from_user.id, FindHotelState.n_photo, message.chat.id)
    elif message.text.lower() in ['нет', 'no', 'не', 'не надо', 'не нужно', 'без фото', '-']:
        bot.send_message(message.from_user.id, 'Нет, так нет')
        message.text = '0'
        get_n_photo(message)
    else:
        bot.send_message(message.from_user.id, 'Я вас не понял. Нужны фото? (да/нет)')


@bot.message_handler(state=FindHotelState.n_photo)
def get_n_photo(message: Message):
    if message.text.isdigit() and 0 <= int(message.text) <= 10:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            for hotel in data['hotel_detail']:
                photo = [InputMediaPhoto(img) for img in hotel["images"][0:int(message.text)]]
                bot.send_message(message.from_user.id,
                                 f"------------------------------\n"
                                 f"Отель: {hotel['name']}\n"
                                 f"Адрес: {hotel['address']}\n"
                                 f"Цена за ночь ($): {hotel['price']}\n"
                                 f"Расстояние до центра (км): {hotel['distance']}\n"
                                 f"Итоговая цена: {hotel['total_price']}\n\n"
                                 )
                if message.text == '1':
                    bot.send_photo(message.from_user.id, hotel["images"][0])
                elif message.text != '0':
                    bot.send_media_group(message.chat.id, media=photo)
            history_commands.save(message.chat.id)
        bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(message.from_user.id, 'Пожалуйста введите число от 1 до 10')
