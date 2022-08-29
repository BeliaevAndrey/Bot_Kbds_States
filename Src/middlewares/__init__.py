from aiogram import Dispatcher
from .db_midware import GetDBUser


def setup(dp: Dispatcher):
    dp.middleware.setup(GetDBUser())
