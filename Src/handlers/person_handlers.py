from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hunderline, hitalic
from aiogram.types import ReplyKeyboardRemove

from loader import dp, bot, data_manager
from states import PersonState

from keyboards import (start_inline_keyboard,
                       numeric_inline_keyboard,
                       item_inline_keyboard,
                       info_inline_keyboard,
                       basket_inline_keyboard)

from keyboards import callback_catcher
from keyboards import commands_default_keyboard

from joker import load_about_info, write_down_questionnaire, pick_up_questionnaire
# from database import BuyerBasket

amount_line = ''
temp_var_for_transmission = []
basket = []
local_id = ''


def make_line(in_dict: dict) -> str:
    """Keeping DRY-principle (6-times used phrase)"""
    amt_key: str = 'amt' if 'amt' in in_dict.keys() else 'count'
    return f'Название товара: {in_dict["name"]}' \
           f'\nКоличество товара: {in_dict[amt_key]}' \
           f'\nОписание: {in_dict["description"]}\n'


# === on-start main menu call
@dp.message_handler(commands=['start'])
async def answer_start_message(message: types.Message, User):
    print(User)
    await message.answer(text=f'{hbold("Привет")}, {hitalic(message.from_user.first_name)}',
                         reply_markup=start_inline_keyboard)
    await message.answer(text=f'{hitalic("Дополнительные команды:")}{chr(11015)}',
                         reply_markup=commands_default_keyboard)


# == Here is the FSM section
@dp.message_handler(text=['/find', 'найти', 'Найти', 'Ищи', 'ищи', 'Искать', 'искать',
                          'search', 'Search', 'Find', 'find', 'Seek', 'seek'])
async def get_item_name(message: types.Message):
    await message.answer(text=f'{hunderline("Введите название товара")}')
    await PersonState.wait_item_name.set()


@dp.message_handler(state=PersonState.wait_item_name)
async def get_item_name(message: types.Message, state: FSMContext):
    item_index, item_info = data_manager.search_item_by_name(message.text)
    if isinstance(item_info, dict):
        out_line = make_line(item_info)
        await message.answer(text=out_line)
        await state.update_data(item_info_in_data=item_info)
        # data = {'item_info_in_data': item_info}
        # await state.set_data(data)
        # await state.update_data(data)
    else:
        await message.answer(text=f'{hbold("Товар не найден")}{chr(129488)}')
    await state.reset_state(with_data=False)


@dp.message_handler(text=['test', 'тест'])
async def get_data_from_state(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data['item_info_in_data'])

    await message.answer(text=f'{data}')


# == default keyboard section
@dp.message_handler(content_types=['contact'])
async def answer_item_command(message: types.message):
    print(message)
    if message.from_user.id == message.contact.user_id:
        await message.answer(text='Это твой контакт')
    else:
        await message.answer(text='А это кто?')


@dp.message_handler(commands=['Hide'])
async def answer_item_command(message: types.Message):
    await message.answer(text='Hiding keyboard', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(commands='location')
async def answer_get_location(message: types.message):
    await message.answer(text=f'Координаты: {message.location.latitude}, {message.location.longitude}')


# === call main menu
@dp.callback_query_handler(callback_catcher.filter(for_data='switch', b_id='main_menu'))
async def answer_kbd_command(call: types.CallbackQuery):
    await bot.send_message(text='Главное меню',
                           chat_id=call.message.chat.id,
                           reply_markup=start_inline_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)


# === call basket menu
@dp.callback_query_handler(callback_catcher.filter(for_data='switch', b_id='scroll_basket'))
async def answer_kbd_command(call: types.CallbackQuery):
    await bot.send_message(text='Меню корзины',
                           chat_id=call.message.chat.id,
                           reply_markup=basket_inline_keyboard())
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)


# === call information section
@dp.callback_query_handler(callback_catcher.filter(for_data='info', b_id='info'))
async def answer_kbd_command(call: types.CallbackQuery):
    await bot.send_message(text='Информация',
                           chat_id=call.message.chat.id,
                           reply_markup=info_inline_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)


# == information section keyboard
@dp.callback_query_handler(callback_catcher.filter(for_data='inform'))
async def answer_info_kbd_command(call: types.CallbackQuery):
    operand = call.data.split(':')[-1]
    line_out = 'still empty'
    if operand == 'hours':
        line_out = 'Пн.-Пт.\n10:00-19:00\n12:00-15:00 -- На огороде.'

    elif operand == 'Our contacts':
        line_out = 'Planet Earth'\
                   '\nLand of Bots'\
                   '\nCyborg city'\
                   '\nCurved avenue, 14, penthouse'\
                   '\n8 (800) TRY-FIND'

    elif operand == 'about_us':
        line_out = f'{load_about_info()}'

    elif operand == 'about_bot':
        line_out = 'Telegram bot (c) 2022 v 2E-3.beta'

    await call.message.answer(text=line_out,
                              reply_markup=info_inline_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)


# == showcase section
@dp.callback_query_handler(callback_catcher.filter(for_data='showcase', b_id='showcase'))
async def answer_kbd_command(call: types.CallbackQuery):
    await bot.send_message(text=f'Ассортимент:\n{data_manager.get_showcase()}',
                           chat_id=call.message.chat.id,
                           reply_markup=start_inline_keyboard)
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)


# ==  scroll showcase step by step I
@dp.callback_query_handler(callback_catcher.filter(for_data='purchase'))
async def answer_kbd_command(call: types.CallbackQuery, Basket_on_CB, User_on_CB):
    print(Basket_on_CB.new(User_on_CB))     # TODO: print is actually redundant here
    global local_id, basket
    local_id = call.data.split(':')[-1]
    if local_id != '':
        status, item_info = data_manager.get_item(int(local_id))
        out_line = make_line(item_info)
    else:
        status = 'ok'
        out_line = 'Товар не определен. Выберите на витрине.'
    await bot.send_message(text=out_line,
                           chat_id=call.message.chat.id,
                           reply_markup=item_inline_keyboard(item_index=local_id,
                                                             status=status))
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)


# ==  scroll showcase step by step II
@dp.callback_query_handler(callback_catcher.filter(for_data='purchase'))
@dp.callback_query_handler(callback_catcher.filter(for_data='scroll'))
async def answer_kbd_command(call: types.CallbackQuery, User_on_CB, Basket_on_CB):
    print(Basket_on_CB.new(User_on_CB))     # TODO: print is actually redundant here
    print(Basket_on_CB.show_basket(User_on_CB))
    global local_id
    local_id = call.data.split(':')[-1]
    status, item_info = data_manager.get_item(int(local_id))
    out_line = make_line(item_info)
    await bot.send_message(text=out_line,
                           chat_id=call.message.chat.id,
                           reply_markup=item_inline_keyboard(item_index=local_id,
                                                             status=status))
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)


# === call 'buy_it' section
@dp.callback_query_handler(callback_catcher.filter(for_data='do_want'))
async def answer_kbd_command(call: types.CallbackQuery):
    global local_id
    local_id = call.data.split(':')[-1]
    status, item_info = data_manager.get_item(int(local_id))
    out_line = make_line(item_info)
    await bot.send_message(text=out_line,
                           chat_id=call.message.chat.id,
                           reply_markup=numeric_inline_keyboard())
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)


# == call numeric keyboard
@dp.callback_query_handler(callback_catcher.filter(for_data='nums'))
async def answer_kbd_command(call: types.CallbackQuery, User_on_CB, Basket_on_CB):
    global amount_line, basket, local_id
    if local_id != '':
        status, item_info = data_manager.get_item(int(local_id))
        out_line = make_line(item_info)
    else:
        out_line = 'Товар не определен. Выберите на витрине.'
    operand = call.data.split(':')[-1]
    if operand == '+':
        out_line = ''
        amount_line = '1' if amount_line in ('', '0') else str(int(amount_line) + 1)
    elif operand == '-':
        out_line = ''
        amount_line = str(int(amount_line) - 1) if amount_line not in ('', '0') else ''
        await call.message.answer(text=f'error')
    elif operand == 'append':
        if amount_line not in ('', '0'):
            tmp, amt = data_manager.pick_up_item(int(local_id), int(amount_line))
            if isinstance(tmp, dict):
                tmp['amt'] = amt
                basket.append(tmp)
                print(Basket_on_CB.add_item(User_on_CB, tmp))
                out_line = 'Ok.'
                del tmp
            else:
                out_line = tmp
                del tmp
            amount_line = ''
    elif operand == 'basket':
        out_line = Basket_on_CB.show_basket(User_on_CB)
        # for item in basket:
        #     out_line += f"{item['name']}" \
        #                f"\n{item['amt']} шт" \
        #                f"\n{'='*10}\n"
    elif operand == 'clear_cur':
        out_line = ''
        amount_line = ''
    elif operand == 'clear_all':
        amount_line = ''
        basket = []
        out_line = 'You\'ve just emptied basket'
    else:
        out_line = ''
        amount_line += operand if operand.isdigit() else ''

    await call.message.answer(text=f'{out_line}'
                                   f'\nAmount: {amount_line.lstrip("0")}',
                              reply_markup=numeric_inline_keyboard())
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


# === call scroll-basket section
@dp.callback_query_handler(callback_catcher.filter(for_data='bskt_scroll'))
async def answer_kbd_command(call: types.CallbackQuery, User_on_CB, Basket_on_CB):
    print(User_on_CB)
    print(Basket_on_CB.show_basket(User_on_CB))
    active_pos = 0
    status = 'Ok'
    global basket
    if not basket:
        out_line = 'Корзина пуста. Положите в нее что-нибудь нужное.'
    elif call.data.split(':')[-1] == 'clr_bskt':
        for tmp in basket:
            print(data_manager.add_item(tmp['id'], tmp['name'], tmp['description'], tmp['amt'], ))
        basket = []
        out_line = 'Корзина очищена.'
    elif call.data.split(':')[-1] == 'clr_pos':
        tmp_b_cls = Basket_on_CB.remove_item(User_on_CB, active_pos)
        print(tmp_b_cls)
        tmp = basket.pop(active_pos)
        out_line = 'Позиция ' + tmp['name'] + ' удалена.'
        data_manager.add_item(tmp['id'], tmp['name'], tmp['description'], tmp['amt'])
        del tmp
    else:
        item_info = Basket_on_CB.show_position(User_on_CB, active_pos)
        print(f'func scroll bask\n{item_info}')
        active_pos = int(call.data.split(':')[-1])
        item_info1 = basket[active_pos]
        status = 'Ok'
        if active_pos == 0:
            status = 'low'
        elif active_pos == len(basket) - 1:
            status = 'high'
        out_line = make_line(item_info1)
    await bot.send_message(text=out_line,
                           chat_id=call.message.chat.id,
                           reply_markup=basket_inline_keyboard(item_index=active_pos,
                                                               status=status,
                                                               lim=(len(basket)-1)))
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)


# == Here is the questionnaire FSM section
@dp.message_handler(text=['/questionnaire'])
async def start_questions(message: types.Message, state: FSMContext):
    print(type(message.from_user.id), message.from_user.id)
    print()
    print(pick_up_questionnaire().keys())
    if str(message.from_user.id) in pick_up_questionnaire().keys():
        await message.answer(text='Вы уже проходили опрос.'
                                  '\nМожете посмотреть ответы введя: `my answers`')
    else:
        await message.answer(text="Ну что, начнём? (cancel -- отказаться)")
        answers = {'fin': "0",
                   'uid': str(message.from_user.id)}
        await state.update_data(answers)
        await PersonState.wait_question.set()


@dp.message_handler(state=PersonState.wait_question)
async def get_answer(message: types.Message, state: FSMContext):
    if message.text.lower() == 'cancel':
        await state.reset_state()
        return

    questions = ['Вы любите овощи?',
                 'А овощи Вас любят?',
                 'Сколько звезд не на небе?',
                 'Какова цена дров на Марсе?',
                 'Сколько литров воды весит 1 кг пуха?']
    answers = await state.get_data()
    i = int(answers['fin'])
    answers[str(i)] = message.text
    answers['fin'] = str(i + 1)
    if i == len(questions):
        await state.reset_state(with_data=False)
        await message.answer(text='Хорошо. Спасибо за ваши ответы.')
        answers['questions'] = questions
        answers.pop('fin')
        answers.pop('0')
        write_down_questionnaire(answers)
        await state.reset_state()
    else:
        await message.answer(text=questions[i])
        await state.update_data(answers)


@dp.message_handler(text=['my answers'])
async def get_answers_back(message: types.Message, state: FSMContext):
    try:
        answers = pick_up_questionnaire()[str(message.from_user.id)]
    except KeyError:
        await message.answer(text='Вы еще не проходили опросник.')
    else:
        line_out = ''
        for item in answers['questions']:
            i = str(int(answers["questions"].index(item)) + 1)
            line_out += f'Q{i}: {item}' \
                        f'\nA: {answers[i]}\n'
        await message.answer(text=f'{line_out}')
    finally:
        await state.reset_state(with_data=False)


@dp.message_handler()
async def answer_ape_yell(message: types.message):
    await message.answer(text=f'Я не понял... Если овощ такой, то нет его.')
