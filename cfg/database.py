import sqlite3
import datetime


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, username):
        with self.connection:
            date_reg = datetime.datetime.now()
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `username`, `date_reg`) VALUES (?, ?, ?)", (user_id, username, date_reg))

    def del_user(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM users WHERE user_id = (?)", (user_id,))

    def get_keyboard(self):
        with self.connection:
            return self.cursor.execute(f"SELECT `city` FROM `keyboard`;").fetchall()

    def get_keyboard_district(self, city):
        with self.connection:
            return self.cursor.execute(f"SELECT `district` FROM `keyboard` WHERE `city` = ?", (city,)).fetchone()

    def get_keyboard_products(self, city):
        with self.connection:
            return self.cursor.execute(f"SELECT `product` FROM `keyboard` WHERE `city` = ?", (city,)).fetchone()

    def get_bot_token(self):
        with self.connection:
            return self.cursor.execute(f"SELECT `TOKEN` FROM `config`;").fetchone()

    def get_all_info(self, name_table):
        with self.connection:
            return self.cursor.execute(f"SELECT `{name_table}` FROM `config`;").fetchone()

    def add_admin(self, new_admin, name_table):
        with self.connection:
            return self.cursor.execute(f"UPDATE config SET {name_table} = {name_table} || '{new_admin}' WHERE `id` = 1;")

    def del_admin(self, id_admin, name_table):
        with self.connection:
            admin_id_all = str(self.cursor.execute(f"SELECT `{name_table}` FROM `config`;").fetchone()[0])
            dl_admin = admin_id_all.split("|")
            try:
                dl_admin.remove(f"{id_admin}")
                if dl_admin:
                    dl_admin = "|".join(dl_admin)
                    return self.cursor.execute(f"UPDATE config SET {name_table} = '{dl_admin}' WHERE `id` = 1;")
                else:
                    return self.cursor.execute(f"UPDATE config SET {name_table} = '' WHERE `id` = 1;")

            except:
                return "Такого нет"

    def edit_min_balance(self, min_b):
        with self.connection:
            return self.cursor.execute(f"UPDATE config SET MIN_BALANCE = '{min_b}' WHERE `id` = 1;")

    def get_all_data(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users`").fetchall()

    def add_city(self, city_name):
        with self.connection:
            return self.cursor.execute("INSERT INTO `keyboard` (`city`) VALUES (?)", (city_name,))

    def del_city(self, city_name):
        with self.connection:
            return self.cursor.execute("DELETE FROM `keyboard` WHERE city = (?)", (city_name,))

    def del_district(self, name_district, name_table, name_city):
        with self.connection:
            admin_id_all = str(self.cursor.execute(f"SELECT `{name_table}` FROM `keyboard` WHERE `city` = (?);", (name_city,)).fetchone()[0])
            dl_admin = admin_id_all.split("|")
            try:
                dl_admin.remove(f"{name_district}")
                if dl_admin:
                    dl_admin = "|".join(dl_admin)
                    return self.cursor.execute(f"UPDATE keyboard SET {name_table} = '{dl_admin}' WHERE `city` = (?);", (name_city,))
                else:
                    return self.cursor.execute(f"UPDATE keyboard SET {name_table} = '' WHERE `city` = (?);", (name_city,))

            except:
                return "Такого нет"

    def add_district(self, name_city, name_table, name_district):
        with self.connection:
            a = self.cursor.execute(f"SELECT `{name_table}` FROM `keyboard` WHERE `city` = ?", (name_city,)).fetchone()[0]
            if a:
                return self.cursor.execute(f"UPDATE keyboard SET {name_table} = {name_table} || '{name_district}' WHERE `city` = (?);", (name_city,))
            else:
                return self.cursor.execute(f"UPDATE keyboard SET {name_table} = '{name_district[1:]}' WHERE `city` = (?);", (name_city,))

    def get_all_malling(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `malling`").fetchall()

    def get_all_user(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id FROM `users`").fetchall()

    def add_malling(self, time, text_malling):
        with self.connection:
            return self.cursor.execute("INSERT INTO `malling` (`time`, `text_malling`) VALUES (?, ?)", (time, text_malling,))

    def edit_com(self, min_b):
        with self.connection:
            return self.cursor.execute(f"UPDATE config SET COMMISSION = '{min_b}' WHERE `id` = 1;")

    def update_token(self, token):
        with self.connection:
            return self.cursor.execute(f"UPDATE config SET TOKEN = '{token}' WHERE `id` = 1;")

    def update_pid(self, pid):
        with self.connection:
            return self.cursor.execute(f"UPDATE config SET PID = '{pid}' WHERE `id` = 1;")