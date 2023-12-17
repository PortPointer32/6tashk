import os
import requests
import subprocess
from openpyxl import Workbook
from datetime import datetime
from aiogram.types import Message
from aiogram.dispatcher import FSMContext, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from main_telegram_bot.utils import StatesAdmin, StatesMal
from main_telegram_bot.KeyboardButton import BUTTON_TYPES
from main_telegram_bot.messages import MESSAGES
from create_main_bot import dp, bot
from cfg.database import Database


scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
scheduler.start()

db = Database('/home/str/6tashk/cfg/database')


# ===================================================
# ================= СОЗДАНИЕ EXCEL ==================
# ===================================================
def write_to_excel_all_users(data, filename):
    workbook = Workbook()
    sheet = workbook.active
    headers = ["id", "user_id", "username", "Дата регистрации"]
    sheet.append(headers)
    for row in data:
        sheet.append(row)
    workbook.save(filename)


# ===================================================
# ================== СТАРТ КОМАНДА ==================
# ===================================================
async def start_command(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["start_admin"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ===================================================
# ===================== АДМИНКА =====================
# ===================================================
# ===== ДОБАВИТЬ/УДАЛИТЬ АДМИНА | ИЗМЕНИТЬ MIN ======
async def add_admin(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        if message.text.lower() == 'добавить админа':
            text_mes = MESSAGES["add_admin"]
        elif message.text.lower() == "удалить админа":
            text_mes = MESSAGES["del_admin"]
        else:
            text_mes = MESSAGES["edit_min"]

        await bot.send_message(chat_id=message.from_user.id, text=text_mes, reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
        state = dp.current_state(user=message.from_user.id)
        await state.update_data(what_admin=message.text)
        await state.set_state(StatesAdmin.all()[0])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# =============== ВВОД ID АДМИНА ===============
async def id_admin(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    elif message.text.isnumeric():
        data = await state.get_data()
        if data["what_admin"] == "Добавить админа":
            db.add_admin(f"|{message.text}", "ADMIN_ID")
            text_mes = "Добавил!"
        elif data["what_admin"] == "Удалить админа":
            db.del_admin(message.text, "ADMIN_ID")
            text_mes = "Удалил!"
        else:
            db.edit_min_balance(message.text)
            text_mes = "Изменил!"

        await message.answer(text=text_mes, reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        await message.answer(MESSAGES["not_admin_id"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        await state.set_state(StatesAdmin.all()[0])


# ===================================================
# ===================== ВСЕ АДМИНЫ ==================
# ===================================================
async def view_all_admin(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        try:
            all_id_admin = db.get_all_info("ADMIN_ID")[0].split("|")
            text = "Все админы:\n\n"
            for idx, admin in enumerate(all_id_admin):
                text += f"{idx+1}.  <code>{admin}</code>\n"
        except:
            all_id_admin = db.get_all_info("ADMIN_ID")[0]
            text = f"Все админы:\n\n1.  <code>{all_id_admin}</code>"
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"], parse_mode="HTML")
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ===================================================
# ================== ДОБАВИТЬ БОТА ==================
# ===================================================
async def add_bot_start(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_new_bot"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesAdmin.all()[1])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# =============== ВВОД TOKEN БОТА ===============
async def input_token_bot(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        all_token = db.get_bot_token()[0]
        my_pid = db.get_all_info("PID")[0]

        try:
            token = all_token.split("|")
            if message.text in token:
                await message.answer("Такой бот уже запущен!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            else:
                db.add_admin(f"|{message.text}", "TOKEN")
                # ЗАПУСК
                os.kill(int(my_pid), 9)
                subprocess.Popen(["/home/str/6tashk/.venv/bin/python", "/home/str/6tashk/start_all_bot.py"])

                await message.answer(MESSAGES['accept_new_bot'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        except:
            db.add_admin(f"|{message.text}", "TOKEN")
            # ЗАПУСК
            os.kill(int(my_pid), 9)
            subprocess.Popen(["/home/str/6tashk/.venv/bin/python", "/home/str/6tashk/start_all_bot.py"])
            
            await message.answer(MESSAGES['accept_new_bot'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()


# ===================================================
# ================== ДОБАВИТЬ ОПЛАТУ ================
# ===================================================
async def add_pay(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        if message.text.lower() == 'добавить карту':
            text_mes = MESSAGES["add_card"]
        elif message.text.lower() == "добавить btc":
            text_mes = MESSAGES["add_btc"]
        else:
            text_mes = MESSAGES["add_ltc"]

        await bot.send_message(chat_id=message.from_user.id, text=text_mes, reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
        state = dp.current_state(user=message.from_user.id)
        await state.update_data(what_admin=message.text)
        await state.set_state(StatesAdmin.all()[2])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# =============== ВВОД КОШЕЛЬКА ===============
async def input_data_pay(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        data = await state.get_data()
        if data["what_admin"] == 'Добавить карту':
            db.add_admin(f"|{message.text}", "NUMBER_CARD")
            await message.answer("Карта добавлена!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            await state.finish()

        else:
            await state.update_data(number_pay=message.text)
            await message.answer(MESSAGES["photo_pay"], reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesAdmin.all()[3])


# =============== ВВОД ФОТО QR ===============
async def input_photo_qr(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        await message.photo[-1].download(f'img/{data["number_pay"]}.jpg')
        if data["what_admin"] == "Добавить BTC":
            db.add_admin(f"|{data['number_pay']}", "NUMBER_BTC")
        else:
            db.add_admin(f"|{data['number_pay']}", "NUMBER_LTC")

        await message.answer("Новый счёт добавлен!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    except:
        if message.text.lower() == "отмена":
            await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            await state.finish()
        else:
            await message.answer("Это не фото QR\nПопробуй снова:", reply_markup=BUTTON_TYPES["BTN_CANCEL"])
            await state.set_state(StatesAdmin.all()[3])


# ===================================================
# =================== УДАЛИТЬ ОПЛАТУ ================
# ===================================================
async def del_pay(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        if message.text.lower() == 'удалить карту':
            text_mes = MESSAGES["del_card"]
        elif message.text.lower() == "удалить btc":
            text_mes = MESSAGES["del_btc"]
        else:
            text_mes = MESSAGES["del_ltc"]

        await bot.send_message(chat_id=message.from_user.id, text=text_mes, reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
        state = dp.current_state(user=message.from_user.id)
        await state.update_data(what_admin=message.text)
        await state.set_state(StatesAdmin.all()[4])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# =============== УДАЛЕНИЕ КОШЕЛЬКА ===============
async def input_pay_for_del(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        try:
            data = await state.get_data()
            if data["what_admin"] == 'Удалить карту':
                what_pay = "NUMBER_CARD"
            elif data["what_admin"] == "Удалить BTC":
                what_pay = "NUMBER_BTC"
                os.remove(f"img/{message.text}.jpg")
            else:
                what_pay = "NUMBER_LTC"
                os.remove(f"img/{message.text}.jpg")

            what_del = db.del_admin(message.text, what_pay)
            if what_del == "Такого нет":
                await message.answer("Такого счёта нет!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            else:
                await message.answer("Счёт удалён!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        except:
            await message.answer("Такого счёта нет!", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()


# ===================================================
# ==================== ВСЕ КОШЕЛЬКИ =================
# ===================================================
async def all_wallets(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        NUMBER_CARD = db.get_all_info("NUMBER_CARD")[0].split("|")
        NUMBER_BTC = db.get_all_info("NUMBER_BTC")[0].split("|")
        NUMBER_LTC = db.get_all_info("NUMBER_LTC")[0].split("|")

        text = "<b>ВСЕ ПРИВЯЗАННЫЕ СЧЕТА К МАГАЗИНАМ:</b>\n\n\n<u>Банковские карты</u>\n"

        for idx, card in enumerate(NUMBER_CARD):
            text += f"<b>{idx+1}.</b> <code>{card}</code>\n"

        text += "\n<u>BTC счёт</u>\n"
        for idx, btc in enumerate(NUMBER_BTC):
            text += f"<b>{idx+1}.</b> <code>{btc}</code>\n"

        text += "\n<u>LTC счёт</u>\n"
        for idx, ltc in enumerate(NUMBER_LTC):
            text += f"<b>{idx+1}.</b> <code>{ltc}</code>\n"

        await message.answer(text, reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"], parse_mode="HTML")

    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ===================================================
# ================== ВСЕ ПОЛЬЗОВАТЕЛИ ===============
# ===================================================
async def all_users_reg(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        write_to_excel_all_users(db.get_all_data(), "все_пользователи.xlsx")
        with open("все_пользователи.xlsx", 'rb') as file:
            await bot.send_document(message.from_user.id, file, reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        os.remove("все_пользователи.xlsx")
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ===================================================
# ============ ДОБАВИТЬ/УДАЛИТЬ ГОРОД ===============
# ===================================================
async def add_del_city(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        if message.text.lower() == 'добавить город':
            await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_city"], reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
        else:
            await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["del_city"], reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
            all_name_city = db.get_keyboard()
            text = "<b>Все города в боте:</b>\n\n"
            for idx, name_city in enumerate(all_name_city):
                text += f"<b>{idx+1}.</b> <code>{name_city[0]}</code>\n"

            await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")

        state = dp.current_state(user=message.from_user.id)
        await state.update_data(what_city=message.text)
        await state.set_state(StatesAdmin.all()[5])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# =============== ВВОД ГОРОДА ===============
async def input_city_name(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        data = await state.get_data()
        if data["what_city"] == "Добавить Город":
            db.add_city(message.text)
            text_mes = "Добавил!"
        else:
            db.del_city(message.text)
            text_mes = "Удалил!"

        await message.answer(text=text_mes, reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()


# ===================================================
# ============ ДОБАВИТЬ/УДАЛИТЬ РАЙОН ===============
# ===================================================
async def add_del_district(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        text = MESSAGES["what_city"]
        all_name_city = db.get_keyboard()
        text += "\n\n<b>Все города в боте:</b>\n"
        for idx, name_city in enumerate(all_name_city):
            text += f"<b>{idx+1}.</b> <code>{name_city[0]}</code>\n"
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")

        state = dp.current_state(user=message.from_user.id)
        await state.update_data(what_city=message.text)
        await state.set_state(StatesAdmin.all()[6])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ============ ДОБАВИТЬ/УДАЛИТЬ РАЙОН ===============
async def for_which_city(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        data = await state.get_data()
        if data["what_city"] == 'Добавить Район':
            await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_district"], reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
            await state.update_data(name_dis=message.text)
            await state.set_state(StatesAdmin.all()[7])
        else:
            try:
                text = ""
                if data["what_city"].lower() == 'добавить район' or data["what_city"].lower() == 'удалить район':
                    text = MESSAGES["del_district"]

                all_name_city = db.get_keyboard_district(message.text)[0].split("|")
                text += "\n\n<b>Все Районы в боте:</b>\n"
                for idx, name_city in enumerate(all_name_city):
                    text += f"<b>{idx+1}.</b> <code>{name_city}</code>\n"

                await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
                await state.update_data(name_dis=message.text)
                if data["what_city"].lower() == 'добавить район' or data["what_city"].lower() == 'удалить район':
                    await state.set_state(StatesAdmin.all()[7])
                else:
                    await state.set_state(StatesAdmin.all()[8])
            except:
                await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_district"], reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
                await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
                await state.finish()


# =============== ВВОД РАЙОНА ===============
async def input_district_name(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        data = await state.get_data()
        if data["what_city"] == 'Добавить Район':
            db.add_district(data["name_dis"], "district", f"|{message.text}")
            text_mes = "Добавил!"
        else:
            db.del_district(message.text, "district", data["name_dis"])
            text_mes = "Удалил!"

        await message.answer(text=text_mes, reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()


# ===================================================
# ============ ДОБАВИТЬ/УДАЛИТЬ РАЙОН ===============
# ===================================================
async def input_product_name(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        data = await state.get_data()
        if data["what_city"].lower() == 'добавить продукт':
            await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_product"], reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
            await state.update_data(raion=message.text)
            await state.set_state(StatesAdmin.all()[9])
        else:
            try:
                text = MESSAGES["del_product"]
                all_name_city = db.get_keyboard_products(data["name_dis"])[0].split("|")
                text += "\n\n<b>Все Продукты в этом районе:</b>\n"
                for idx, name_city in enumerate(all_name_city):
                    if message.text in name_city:
                        text += f"<b>{idx+1}.</b> <code>{name_city}</code>\n"

                await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
                await state.update_data(raion=message.text)
                await state.set_state(StatesAdmin.all()[9])

            except:
                await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_district"], reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
                await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
                await state.finish()


# =============== ВВОД ПРОДУКТА ===============
async def add_del_product_name(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()
    else:
        data = await state.get_data()
        if data["what_city"] == "Добавить Продукт":
            db.add_district(data["name_dis"], "product", f"|{message.text}({data['raion']})")
            text_mes = "Добавил!"
        else:
            db.del_district(message.text, "product", data["name_dis"])
            text_mes = "Удалил!"

        await message.answer(text=text_mes, reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await state.finish()


# ===================================================
# ================ СДЕЛАТЬ РАССЫЛКУ =================
# ===================================================
async def add_malling(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["add_malling"], reply_markup=BUTTON_TYPES["BTN_CANCEL"], parse_mode="HTML")
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(StatesMal.all()[0])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# =============== ПРОВЕРКА РАССЫЛКИ ===============
async def input_malling(message: Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await message.answer(MESSAGES['start_admin'], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        try:
            int(message.text[0:2])
            int(message.text[3:5])
            time = message.text[0:5]
            text_malling = message.text[6:]
            db.add_malling(time, text_malling)
            await message.answer(text=MESSAGES["accept_malling"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
            try:
                # РАССЫЛКА
                all_info_malling = db.get_all_malling()[-1]
                scheduler.add_job(send_m, trigger='cron', hour=all_info_malling[1][0:2],
                                  minute=all_info_malling[1][3:5],
                                  start_date=datetime.now(), kwargs={"text_malling": all_info_malling[-1]},
                                  id=f"{message.message_id}_{message.from_user.id}")
                await bot.send_message(text=f"Рассылка зарегистрирована!\n\nВремя рассылки: {all_info_malling[1][0:5]}"
                                            f"\nТекст рассылки: {all_info_malling[-1]}\n\nId рассылки: <code>{message.message_id}_{message.from_user.id}</code>",
                                       chat_id=message.from_user.id, parse_mode="HTML")
            except:
                await bot.send_message(text="Рассылка была создана не верно!", chat_id=message.from_user.id)
        except:
            await message.answer(text=MESSAGES["no_malling"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])

    await state.finish()


# ===================================================
# ================ ОСТАНОВКА РАССЫЛКИ ===============
# ===================================================
async def stop_malling(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        try:
            scheduler.remove_job(f"{message.text[6:]}")
            await bot.send_message(text="Рассылка остановлена!", chat_id=message.from_user.id)
        except:
            await bot.send_message(text="Такой рассылки нет", chat_id=message.from_user.id)


# ===================================================
# ================= ФУНКЦИЯ РАССЫЛКИ ================
# ===================================================
async def send_m(text_malling):
    all_id_users = db.get_all_user()
    all_token = db.get_bot_token()[0].split("|")
    for token in all_token:
        for id_user in all_id_users:
            try:
                url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + str(id_user[0]) + "&text=" + text_malling
                requests.get(url_req)
            except:
                ...


# ===================================================
# =============== ИЗМЕНЕНИЕ КОМИССИИ ================
# ===================================================
async def edit_commission(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        db.edit_com(message.text[5:])
        await bot.send_message(chat_id=message.from_user.id, text="Комиссия в магазине изменина", reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["start_admin"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


# ===================================================
# =============== НЕИЗВЕСТНАЯ КОМАНДА ===============
# ===================================================
async def unknown_command(message: Message):
    ADMIN_ID = db.get_all_info("ADMIN_ID")[0]
    if str(message.from_user.id) in str(ADMIN_ID):
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["start_admin"], reply_markup=BUTTON_TYPES["BTN_HOME_ADMIN"])
    else:
        await bot.send_message(chat_id=message.from_user.id, text=MESSAGES["not_command"])


def register_handler_admin(dp: Dispatcher):
    # СТАРТ
    dp.register_message_handler(start_command, lambda message: message.text == '/start' or message.text == 'Главное меню')
    dp.register_message_handler(stop_malling, lambda message: '/stop' in message.text)

    # ИЗМЕНЕНИЕ КОМИССИИ
    dp.register_message_handler(edit_commission, lambda message: '/com' in message.text)

    # ДОБАВИТЬ/УДАЛИТЬ АДМИНА | ИЗМЕНИТЬ MIN
    dp.register_message_handler(add_admin, lambda message: message.text.lower() == 'добавить админа' or message.text.lower() == "удалить админа" or message.text.lower() == "изменить min пополнение")
    dp.register_message_handler(id_admin, state=StatesAdmin.STATES_0)

    # ВСЕ АДМИНЫ
    dp.register_message_handler(view_all_admin, lambda message: message.text.lower() == 'все админы')

    # ДОБАВИТЬ БОТА
    dp.register_message_handler(add_bot_start, lambda message: message.text.lower() == 'добавить бота')
    dp.register_message_handler(input_token_bot, state=StatesAdmin.STATES_1)

    # ДОБАВИТЬ ОПЛАТУ
    dp.register_message_handler(add_pay, lambda message: message.text.lower() == 'добавить карту' or message.text.lower() == 'добавить btc' or message.text.lower() == 'добавить ltc')
    dp.register_message_handler(input_data_pay, state=StatesAdmin.STATES_2)
    dp.register_message_handler(input_photo_qr, state=StatesAdmin.STATES_3, content_types=["photo", "text"])

    # УДАЛИТЬ ОПЛАТУ
    dp.register_message_handler(del_pay, lambda message: message.text.lower() == 'удалить карту' or message.text.lower() == 'удалить btc' or message.text.lower() == 'удалить ltc')
    dp.register_message_handler(input_pay_for_del, state=StatesAdmin.STATES_4)

    # ВСЕ КОШЕЛЬКИ
    dp.register_message_handler(all_wallets, lambda message: message.text.lower() == 'все кошельки')

    # ВСЕ ПОЛЬЗОВАТЕЛИ
    dp.register_message_handler(all_users_reg, lambda message: message.text.lower() == 'все пользователи')

    # ДОБАВИТЬ/УДАЛИТЬ ГОРОД
    dp.register_message_handler(add_del_city, lambda message: message.text.lower() == 'добавить город' or message.text.lower() == 'удалить город')
    dp.register_message_handler(input_city_name, state=StatesAdmin.STATES_5)

    # ДОБАВИТЬ/УДАЛИТЬ РАЙОН
    dp.register_message_handler(add_del_district, lambda message: message.text.lower() == 'добавить район' or message.text.lower() == 'удалить район' or message.text.lower() == 'добавить продукт' or message.text.lower() == 'удалить продукт')
    dp.register_message_handler(for_which_city, state=StatesAdmin.STATES_6)
    dp.register_message_handler(input_district_name, state=StatesAdmin.STATES_7)

    # ДОБАВИТЬ/УДАЛИТЬ ПРОДУКТ
    dp.register_message_handler(input_product_name, state=StatesAdmin.STATES_8)
    dp.register_message_handler(add_del_product_name, state=StatesAdmin.STATES_9)

    # СДЕЛАТЬ РАССЫЛКУ
    dp.register_message_handler(add_malling, lambda message: message.text.lower() == 'сделать рассылку')
    dp.register_message_handler(input_malling, state=StatesMal.STAT_0)

    # НЕИЗВЕСТНАЯ КОМАНДА
    dp.register_message_handler(unknown_command, content_types=["text"])
