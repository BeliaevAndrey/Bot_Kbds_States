from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from database import BuyerBasket


class GetDBUser(BaseMiddleware):
    _buyer_basket = BuyerBasket()

    async def on_process_message(self, message: types.Message, data: dict):
        data['User'] = (message.from_user.id, message.from_user.username, 'Hello from middleware!')
        data['Basket'] = self._buyer_basket

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        data['User_on_CB'] = call.from_user.id
        data['Basket_on_CB'] = self._buyer_basket
