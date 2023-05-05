from states.st_find_hotel import FindHotelState
from loader import bot
from utils import RapidAPI


@bot.callback_query_handler(func=lambda callback: callback.data)
def hotel(callback):

    with bot.retrieve_data(callback.message.chat.id) as data:
        if callback.data in data['cities_dct'].values():
            for city, id in data['cities_dct'].items():
                if callback.data == id:
                    data['cities_dct'] = {city: id}
            print('Выбран: ', data['cities_dct'])
            bot.send_message(callback.message.chat.id, "Введите дату своего прибытия в формате ДД.ММ.ГГ")
            bot.set_state(callback.from_user.id, FindHotelState.date, callback.message.chat.id)

        elif callback.data == 'Все верно':
            bot.send_message(callback.message.chat.id, "Отлично! Ищу отели...")
            data['hotels_lst'] = RapidAPI.hotels(callback.message.chat.id)
            if data['hotels_lst'] is not None:
                bot.send_message(callback.message.chat.id, f"По вашему запросу найдено "
                                                           f"{len(data['hotels_lst'])} отелей.\n\n"
                                                           f"Сколько отелей хотите посмотреть?")
                bot.set_state(callback.message.from_user.id, FindHotelState.quantity, callback.message.chat.id)
            else:
                bot.send_message(callback.message.chat.id, "Жаль...😞 По вашему запросу ничего не найдено\n"
                                                           "Давайте попробуем еще раз, "
                                                           "но с другими параметрами поиска.")

