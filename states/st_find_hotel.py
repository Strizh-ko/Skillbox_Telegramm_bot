from telebot.handler_backends import State, StatesGroup


class FindHotelState(StatesGroup):
    location = State()
    date = State()
    days = State()
    people = State()
    mode = State()