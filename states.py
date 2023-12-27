from aiogram.dispatcher.filters.state import StatesGroup, State


class ProductAddState(StatesGroup):
    name = State()
    price = State()
    photo = State()
    info = State()


class RegisterState(StatesGroup):
    phone_number = State()
    login = State()
    password = State()