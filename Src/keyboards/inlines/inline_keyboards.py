from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_dt import callback_catcher

# == Basic inline keyboard
start_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text=f'Витрина',
                             callback_data=callback_catcher.new(
                                 for_data='showcase',
                                 b_id='showcase'))
    ],
    [
        InlineKeyboardButton(text='К покупкам',
                             callback_data=callback_catcher.new(
                                 for_data='purchase',
                                 b_id='0'))
    ],
    [
        InlineKeyboardButton(text='Сведения',
                             callback_data=callback_catcher.new(
                                 for_data='info',
                                 b_id='info'))
    ],
])


# == scrolling kbd
def item_inline_keyboard(item_index='0', status='low') -> InlineKeyboardMarkup:
    item_inline_kbd = InlineKeyboardMarkup()
    if status == 'high':
        index_left = str(int(item_index) - 1)
        btm = InlineKeyboardButton(text='<<<',
                                   callback_data=callback_catcher.new(
                                       for_data='scroll',
                                       b_id=index_left)
                                   )
        item_inline_kbd.add(btm)
    elif status == 'low':
        index_right = str(int(item_index) + 1)
        btm = InlineKeyboardButton(text='>>>',
                                   callback_data=callback_catcher.new(
                                       for_data='scroll',
                                       b_id=index_right)
                                   )
        item_inline_kbd.add(btm)
    else:
        index_left = str(int(item_index) - 1)
        index_right = str(int(item_index) + 1)
        btm_left = InlineKeyboardButton(text='<<<',
                                        callback_data=callback_catcher.new(
                                            for_data='scroll',
                                            b_id=index_left))
        btm_right = InlineKeyboardButton(text='>>>',
                                         callback_data=callback_catcher.new(
                                             for_data='scroll',
                                             b_id=index_right))
        item_inline_kbd.row(btm_left, btm_right)

    item_inline_kbd.add(InlineKeyboardButton(text='Хочу!',
                                             callback_data=callback_catcher.new(
                                                 for_data='do_want',
                                                 b_id=item_index)))
    item_inline_kbd.add(InlineKeyboardButton(text='Смотреть корзину',
                                             callback_data=callback_catcher.new(for_data='switch',
                                                                                b_id='scroll_basket'
                                                                                )))
    item_inline_kbd.add(InlineKeyboardButton(text='Главное меню',
                                             callback_data=callback_catcher.new(for_data='switch',
                                                                                b_id='main_menu'
                                                                                )))
    return item_inline_kbd


# == numeric keyboard
def numeric_inline_keyboard() -> InlineKeyboardMarkup:
    num_inline_kbd = InlineKeyboardMarkup()
    btns = []
    for i in range(10):
        btns.append(InlineKeyboardButton(text=str(i),
                                         callback_data=callback_catcher.new(
                                             for_data='nums',
                                             b_id=str(i))))
    plus = InlineKeyboardButton(text='+',
                                callback_data=callback_catcher.new(
                                    for_data='nums',
                                    b_id='+'))
    minus = InlineKeyboardButton(text='-',
                                 callback_data=callback_catcher.new(
                                     for_data='nums',
                                     b_id='-'))
    append_btn = InlineKeyboardButton(text='Добавить',
                                      callback_data=callback_catcher.new(
                                          for_data='nums',
                                          b_id='append'))
    basket_btn = InlineKeyboardButton(text='Корзинка',
                                      callback_data=callback_catcher.new(
                                          for_data='nums',
                                          b_id='basket'))
    clear_cur = InlineKeyboardButton(text='Сброс',
                                     callback_data=callback_catcher.new(
                                         for_data='nums',
                                         b_id='clear_cur'))
    # clear_all = InlineKeyboardButton(text='Сброс корзины',
    #                                  callback_data=callback_catcher.new(
    #                                      for_data='nums',
    #                                      b_id='clear_all'))

    num_inline_kbd.row(btns[1], btns[2], btns[3])
    num_inline_kbd.row(btns[4], btns[5], btns[6])
    num_inline_kbd.row(btns[7], btns[8], btns[9])
    num_inline_kbd.row(minus, btns[0], plus)
    num_inline_kbd.row(append_btn, basket_btn, clear_cur)

    num_inline_kbd.add(InlineKeyboardButton(text='К покупкам',
                                            callback_data=callback_catcher.new(
                                                for_data='purchase',
                                                b_id='0')))
    
    num_inline_kbd.add(InlineKeyboardButton(text='Главное меню',
                                            callback_data=callback_catcher.new(for_data='switch',
                                                                               b_id='main_menu'
                                                                               )))
    return num_inline_kbd


# == information keyboard
info_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Часы работы',
                                 callback_data=callback_catcher.new(for_data='inform',
                                                                    b_id='hours'))
        ],
        [
            InlineKeyboardButton(text='Контакты',
                                 callback_data=callback_catcher.new(for_data='inform',
                                                                    b_id='Our contacts'))
        ],
        [
            InlineKeyboardButton(text='О нас',
                                 callback_data=callback_catcher.new(for_data='inform',
                                                                    b_id='about_us'))
        ],
        [
            InlineKeyboardButton(text='О Боте',
                                 callback_data=callback_catcher.new(for_data='inform',
                                                                    b_id='about_bot'))
        ],
        [
            InlineKeyboardButton(text='Главное меню',
                                 callback_data=callback_catcher.new(for_data='switch',
                                                                    b_id='main_menu'))
        ]
    ])


# == basket scroll kbd
def basket_inline_keyboard(item_index='0', status='low', lim: int = 0) -> InlineKeyboardMarkup:
    basket_inline_kbd = InlineKeyboardMarkup()
    if status == 'high':
        index_left = str(int(item_index) - 1) if int(item_index) > 0 else item_index
        btm = InlineKeyboardButton(text='<<<',
                                   callback_data=callback_catcher.new(
                                       for_data='bskt_scroll',
                                       b_id=index_left)
                                   )
        basket_inline_kbd.add(btm)
    elif status == 'low':
        index_right = str(int(item_index) + 1) if int(item_index) < lim else item_index
        btm = InlineKeyboardButton(text='>>>',
                                   callback_data=callback_catcher.new(
                                       for_data='bskt_scroll',
                                       b_id=index_right)
                                   )
        basket_inline_kbd.add(btm)
    else:
        index_left = str(int(item_index) - 1)
        index_right = str(int(item_index) + 1)
        btm_left = InlineKeyboardButton(text='<<<',
                                        callback_data=callback_catcher.new(
                                            for_data='bskt_scroll',
                                            b_id=index_left))
        btm_right = InlineKeyboardButton(text='>>>',
                                         callback_data=callback_catcher.new(
                                             for_data='bskt_scroll',
                                             b_id=index_right))
        basket_inline_kbd.row(btm_left, btm_right)

    clr_basket = InlineKeyboardButton(text='Очистить корзину',
                                      callback_data=callback_catcher.new(
                                          for_data='bskt_scroll',
                                          b_id='clr_bskt'))

    clr_position = InlineKeyboardButton(text='Удалить позицию',
                                        callback_data=callback_catcher.new(
                                            for_data='bskt_scroll',
                                            b_id='clr_pos'))

    basket_inline_kbd.row(clr_position, clr_basket)
    basket_inline_kbd.add(InlineKeyboardButton(text='Главное меню',
                                               callback_data=callback_catcher.new(
                                                   for_data='switch',
                                                   b_id='main_menu')))

    return basket_inline_kbd

