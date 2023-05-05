from telebot.handler_backends import State, StatesGroup


class FindHotelState(StatesGroup):
    location = State()
    date = State()
    days = State()
    people = State()
    quantity = State()
    confirm = State()
    price = State()
    distance = State()
    photo = State()
    n_photo = State()
