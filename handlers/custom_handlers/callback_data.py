from states.st_find_hotel import FindHotelState
from loader import bot
from project import RapidAPI
from keyboards import inline


@bot.callback_query_handler(func=lambda callback: callback.data)
def hotel(callback):

    with bot.retrieve_data(callback.message.chat.id) as data:
        if callback.data in data['cities_dct'].values():
            for city, id in data['cities_dct'].items():
                if callback.data == id:
                    data['cities_dct'] = {city: id}
                    # data['city_name'] = city
                    # data['city_id'] = id
            print(data['cities_dct'])
            bot.send_message(callback.message.chat.id, "Введите дату своего прибытия в формате ДД.ММ.ГГ")

        elif callback.data == 'Все верно':
            bot.send_message(callback.message.chat.id, "Отлично! Ищу отели...")
            data['hotels_lst'] = RapidAPI.hotels(callback.message.chat.id)

            if data['hotels_lst'] != None:
                bot.send_message(callback.message.chat.id, f"По вашему запросу найдено {len(data['hotels_lst'])} отелей.\n\n"
                                                  f"Какие критерии вам важны?", reply_markup=inline.mode.mode_buttons())
                bot.set_state(callback.message.from_user.id, FindHotelState.mode, callback.message.chat.id)
                print(data['hotels_lst'])
            else:
                bot.send_message(callback.message.chat.id, "Жаль...😞 По вашему запросу ничего не найдено\n"
                                                           "Давайте попробуем еще раз, но с другими параметрами поиска.")

        elif callback.data == 'Пока не знаю':
            bot.send_message(callback.message.chat.id, f"Как узнаете, скажите")
