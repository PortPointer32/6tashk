from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# ================= КНОПКИ ПОЛЬЗОВАТЕЛЯ =================

# МЕНЮ
btn_city = InlineKeyboardButton(text="Выберите город", callback_data="city")
btn_balance = InlineKeyboardButton(text="Баланс (0 руб)", callback_data="balance")
btn_my_bot = InlineKeyboardButton(text="Мои боты", callback_data="my_bot")
btn_ref = InlineKeyboardButton(text="Реферальная программа", callback_data="ref")
btn_last_order = InlineKeyboardButton(text="Последний заказ", callback_data="last_order")
btn_operator = InlineKeyboardButton(text="Оператор", url="https://t.me/doggok45")
btn_support = InlineKeyboardButton(text="Тех.поддержка", url="https://t.me/doggok45")

btn_pay = InlineKeyboardButton(text="Оплатить", callback_data="pay_card_p")
btn_menu_home = KeyboardButton("Главное меню")
btn_menu_home_inline = InlineKeyboardButton(text="Главное меню", callback_data="menu_home")

# РЕФЕРАЛЬНАЯ П
btn_add_bot = InlineKeyboardButton(text="Добавить бота", callback_data="add_bot")

# ПОПОЛНЕНИЕ БАЛАНСА
btn_card = InlineKeyboardButton(text='Оплата на карту💳', callback_data="card")
btn_bitcoin = InlineKeyboardButton(text="Bitcoin", callback_data="bitcoin")
btn_ltc = InlineKeyboardButton(text="Litecoin", callback_data="ltc")
btn_problems_pay = InlineKeyboardButton(text="Проблемы с оплатой?", url="https://t.me/doggok45")

btn_cancel = KeyboardButton("Отмена")


BUTTON_TYPES = {
    "BTN_HOME": InlineKeyboardMarkup().add(btn_balance).add(btn_my_bot).add(btn_ref).add(btn_last_order).
    add(btn_operator).add(btn_support),
    "BTN_MENU_HOME": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_menu_home),
    "BTN_ADD_BOT": InlineKeyboardMarkup().add(btn_add_bot).add(btn_menu_home_inline),
    "BTN_MENU": InlineKeyboardMarkup().add(btn_menu_home_inline),
    "BTN_PAY": InlineKeyboardMarkup().add(btn_card).add(btn_bitcoin).add(btn_ltc).add(btn_menu_home_inline),
    "BTN_PROBLEMS": InlineKeyboardMarkup().add(btn_problems_pay),
    "BTN_WHAT_PAY": InlineKeyboardMarkup().add(btn_pay).add(btn_menu_home_inline),

    "BTN_CANCEL": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel),
}
