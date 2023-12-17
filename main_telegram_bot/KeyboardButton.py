from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


# ================= КНОПКИ АДМИНА =================
btn_add_admin = KeyboardButton("Добавить админа")
btn_del_admin = KeyboardButton("Удалить админа")
btn_all_admin = KeyboardButton("Все админы")

btn_add_bot_main = KeyboardButton("Добавить Бота")

btn_add_city = KeyboardButton("Добавить Город")
btn_del_city = KeyboardButton("Удалить Город")

btn_add_district = KeyboardButton("Добавить Район")
btn_del_district = KeyboardButton("Удалить Район")

btn_add_product = KeyboardButton("Добавить Продукт")
btn_del_product = KeyboardButton("Удалить Продукт")

btn_malling = KeyboardButton("Сделать рассылку")
btn_all_info = KeyboardButton("Все пользователи")

btn_add_card = KeyboardButton("Добавить карту")
btn_del_card = KeyboardButton("Удалить карту")

btn_add_btc = KeyboardButton("Добавить BTC")
btn_del_btc = KeyboardButton("Удалить BTC")

btn_add_ltc = KeyboardButton("Добавить LTC")
btn_del_ltc = KeyboardButton("Удалить LTC")

btn_all_wallets = KeyboardButton("Все кошельки")

btn_edit_min = KeyboardButton("Изменить MIN пополнение")

btn_cancel = KeyboardButton("Отмена")


BUTTON_TYPES = {
    "BTN_HOME_ADMIN": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_add_admin, btn_del_admin, btn_all_admin).add(btn_add_bot_main).
    add(btn_add_city, btn_add_district, btn_add_product).add(btn_del_city, btn_del_district, btn_del_product).add(btn_malling).add(btn_all_info).
    add(btn_add_card, btn_add_btc, btn_add_ltc).add(btn_del_card, btn_del_btc, btn_del_ltc).add(btn_all_wallets).add(btn_edit_min),


    "BTN_CANCEL": ReplyKeyboardMarkup(resize_keyboard=True).add(btn_cancel),
}
