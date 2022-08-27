from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


commands_default_keyboard = ReplyKeyboardMarkup(
    keyboard=[
         [
            KeyboardButton(text='/send contact',
                           request_contact=True,),
            KeyboardButton(text='/location',
                           request_location=True)
         ],
         [
            KeyboardButton(text='/Hide keyboard'),
         ]

    ],
    resize_keyboard=True
)
#
# testing_default_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#          [
#             KeyboardButton(text='/test'),
#          ]
#     ],
#     resize_keyboard=True
# )
