from main_telegram_bot.utils import StatesAdmin

# СООБЩЕНИЯ ОТ БОТА
start_message = "Привет 👋"
start_message_2 = "Выберите категори:"

start_admin_message = "Приветствую админ 👋"
not_command_message = "Такой команды нет\nПиши /start"

add_admin_message = """ID состоит только из чисел 
(его можно получить тут @username_to_id_bot)
<b>Вводи ID пользователя для ДОБАВЛЕНИЯ админа:</b>"""
del_admin_message = """ID состоит только из чисел 
(его можно получить тут @username_to_id_bot)
<b>Вводи ID пользователя для УДАЛЕНИЯ админа:</b>"""
not_admin_id_message = """Это не число, ID состоит только из чисел 
 (его можно получить тут @username_to_id_bot)
Вводи ID пользователя:"""
edit_min_message = "Введите значение которое будет использоваться для минимального пополнения:"
add_new_bot_message = "Введите токен для нового магазина:"
accept_new_bot_message = "Новый бот магазин запущен!!!"
add_card_message = "Введите данные <b>БАНКОВСКОЙ КАРТЫ:</b>"
add_btc_message = "Введите данные <b>КОШЕЛЬКА BTC:</b>"
add_ltc_message = "Введите данные <b>КОШЕЛЬКА LTC:</b>"
photo_pay_message = "Отправьте фото QR-кодa в бота:"

del_card_message = "<b>ДЛЯ УДАЛЕНИЯ</b>\nВведите данные <b>БАНКОВСКОЙ КАРТЫ:</b>"
del_btc_message = "<b>ДЛЯ УДАЛЕНИЯ</b>\nВведите данные <b>КОШЕЛЬКА BTC:</b>"
del_ltc_message = "<b>ДЛЯ УДАЛЕНИЯ</b>\nВведите данные <b>КОШЕЛЬКА LTC:</b>"

add_city_message = "Введите название <b>ГОРОДА</b> для <b>ДОБАВЛЕНИЯ:</b>"
del_city_message = "Введите название <b>ГОРОДА</b> для <b>УДАЛЕНИЯ:</b>"

what_city_message = "<u>Введите название ГОРОДА в котором будем выбирать район</u>"

add_district_message = "Введите название <b>РАЙОНА</b> для <b>ДОБАВЛЕНИЯ:</b>"
del_district_message = "Введите название <b>РАЙОНА</b> для <b>УДАЛЕНИЯ:</b>"
not_district_message = "В этом городе нет районов для удаления"

add_product_message = "Введите название <b>ПРОДУКТА</b> для <b>ДОБАВЛЕНИЯ:</b>"
del_product_message = "Введите название <b>ПРОДУКТА</b> для <b>УДАЛЕНИЯ:</b>"

add_malling_message = "<b>Введи текст как в примере:</b>\n\n04:12(время во сколько проводить рассылку)\nЛюбой текст рассылки"

accept_malling_message = "Рассылка добавлена\nЧто бы её запустить, зайдите в нужный магазин и пропишите /start_m"
no_malling_message = "Не правильный формат!"

MESSAGES = {
    "start_user": start_message,
    "start_user_2": start_message_2,
    "start_admin": start_admin_message,
    "not_command": not_command_message,
    "add_admin": add_admin_message,
    "del_admin": del_admin_message,
    "not_admin_id": not_admin_id_message,
    "edit_min": edit_min_message,
    "add_new_bot": add_new_bot_message,
    "accept_new_bot": accept_new_bot_message,
    "add_card": add_card_message,
    "add_btc": add_btc_message,
    "add_ltc": add_ltc_message,
    "photo_pay": photo_pay_message,
    "del_card": del_card_message,
    "del_btc": del_btc_message,
    "del_ltc": del_ltc_message,
    "add_city": add_city_message,
    "del_city": del_city_message,
    "what_city": what_city_message,
    "add_district": add_district_message,
    "del_district": del_district_message,
    "not_district": not_district_message,
    "add_product": add_product_message,
    "del_product": del_product_message,
    "add_malling": add_malling_message,
    "accept_malling": accept_malling_message,
    "no_malling": no_malling_message,
}
