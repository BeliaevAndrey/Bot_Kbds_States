from aiogram.dispatcher.filters.state import StatesGroup, State


class PersonState(StatesGroup):
    wait_item_name = State()
    wait_question = State()
