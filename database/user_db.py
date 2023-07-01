import sqlite3 as sq


class UserDataBase:
    def __init__(self):
        self.connection = sq.connect("database.db")
        self.cursor = self.connection.cursor()

    # Создание пользователя в бд.
    def create_user(self, user_id, first_name=None, user_name=None):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id,first_name,user_name) VALUES (?,?,?)", (user_id, first_name, user_name))

    # Проверка пользователя в бд.
    def check_user(self, user_id):
        user = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchall()
        return bool(len(user))

    # Создание новой сборки.
    def create_accessories(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO assemblies (user_id) VALUES (?)", (user_id,))

    # Удаление сборки пользователя.
    def delete_user_assembling(self, acc_id):
        with self.connection:
            self.cursor.execute("DELETE FROM assemblies WHERE id=?", (acc_id,))

    # Получение не до собравшейся сборки пользователя
    def get_user_assembling(self, user_id):
        assembling = self.cursor.execute("SELECT * FROM assemblies WHERE user_id=? AND status=0", (user_id,)).fetchall()
        return assembling

    # Получение собранных сборок пользователя.
    def get_user_ready_assembling(self, user_id):
        assembling = self.cursor.execute("SELECT * FROM assemblies WHERE user_id=? AND status=1", (user_id,)).fetchall()
        return assembling

    # Получение стадии сборки.
    def get_stage(self, user_id):
        stage = self.cursor.execute("SELECT stage FROM assemblies WHERE user_id=? AND status=0", (user_id,)).fetchone()
        return stage[0]

    # Обновление стадии сборки.
    def update_stage(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE assemblies SET stage = stage+1 WHERE user_id = ? AND status = 0", (user_id,))

    # Получение всех готовых решений
    def get_all_pc(self, type_pc):
        all_pc = self.cursor.execute("SELECT * FROM all_assemblies WHERE type = ?", (type_pc,)).fetchall()
        return all_pc


    # ПОЛУЧЕНИЕ

    def get_type_pc(self, user_id):
        type_pc = self.cursor.execute("SELECT type_pc FROM assemblies WHERE user_id = ? AND status=0", (user_id,)).fetchone()
        return type_pc[0]

    def get_processor(self, user_id):
        motherboard = self.cursor.execute("SELECT motherboard FROM assemblies WHERE user_id = ? AND status=0", (user_id,)).fetchone()[0]
        if motherboard == 1:
            motherboard = self.cursor.execute("SELECT id, name FROM processor WHERE id > 1 ").fetchall()
        else:
            socet_p = self.cursor.execute("SELECT socet_p FROM motherboard WHERE id = ?", (motherboard,)).fetchone()[0]
            motherboard = self.cursor.execute("SELECT id, name FROM processor WHERE id > 1 AND socet_p = ?", (socet_p,)).fetchall()
        return motherboard

    def get_cooler(self):
        cooler = self.cursor.execute("SELECT id, name FROM cooler WHERE id > 1").fetchall()
        return cooler

    def get_body(self):
        body = self.cursor.execute("SELECT id, name FROM body WHERE id > 1").fetchall()
        return body

    def get_drive(self):
        drive = self.cursor.execute("SELECT id, name FROM drive WHERE id > 1").fetchall()
        return drive

    def get_motherboard(self, user_id):
        processor = self.cursor.execute("SELECT processor FROM assemblies WHERE user_id = ? AND status=0", (user_id,)).fetchone()[0]
        if processor == 1:
            motherboard = self.cursor.execute("SELECT id, name FROM motherboard WHERE id > 1").fetchall()
        else:
            socet_p = self.cursor.execute("SELECT socet_p FROM processor WHERE id = ?", (processor,)).fetchone()[0]
            motherboard = self.cursor.execute("SELECT id, name FROM motherboard WHERE id > 1 AND socet_p = ?", (socet_p,)).fetchall()
        return motherboard

    def get_psu(self, user_id):
        TDP_USER = self.cursor.execute("SELECT SUM(processor.TDP+video_card.TDP+400) FROM assemblies JOIN processor ON assemblies.processor = processor.id JOIN video_card ON assemblies.video_card = video_card.id WHERE status = 0 AND user_id = ?", (user_id,)).fetchone()[0]
        psu = self.cursor.execute("SELECT id, name FROM psu WHERE W > ?", (TDP_USER,)).fetchall()
        return psu

    def get_ram(self):
        ram = self.cursor.execute("SELECT id, name FROM ram WHERE id > 1").fetchall()
        return ram

    def get_video_card(self):
        video_card = self.cursor.execute("SELECT id, name FROM video_card WHERE id > 1").fetchall()
        return video_card

    #   ИНФОРМАЦИЯ

    def get_info_processor(self, item_id):
        processor = self.cursor.execute("SELECT description, price, name FROM processor WHERE id = ? ", (item_id,)).fetchone()
        return processor

    def get_info_body(self, item_id):
        body = self.cursor.execute("SELECT description, price, name FROM body WHERE id = ? ", (item_id,)).fetchone()
        return body

    def get_info_cooler(self, item_id):
        cooler = self.cursor.execute("SELECT description, price, name FROM cooler WHERE id = ? ", (item_id,)).fetchone()
        return cooler

    def get_info_drive(self, item_id):
        print(item_id)
        drive = self.cursor.execute("SELECT description, price, name FROM drive WHERE id = ? ", (item_id,)).fetchone()
        return drive

    def get_info_motherboard(self, item_id):
        motherboard = self.cursor.execute("SELECT description, price, name FROM motherboard WHERE id = ? ", (item_id,)).fetchone()
        return motherboard

    def get_info_psu(self, item_id):
        psu = self.cursor.execute("SELECT description, price, name FROM psu WHERE id = ? ", (item_id,)).fetchone()
        return psu

    def get_info_ram(self, item_id):
        ram = self.cursor.execute("SELECT description, price, name FROM ram WHERE id = ? ", (item_id,)).fetchone()
        return ram

    def get_info_video_card(self, item_id):
        video_card = self.cursor.execute("SELECT description, price, name FROM video_card WHERE id = ? ", (item_id,)).fetchone()
        return video_card

    # ОБНОВЛЕНИЕ

    def update_processor(self, user_id, acc_id):
        with self.connection:
            self.cursor.execute("UPDATE assemblies SET processor = ? WHERE user_id = ? AND status = 0", (acc_id, user_id,))

    def update_body(self, user_id, acc_id):
        with self.connection:
            self.cursor.execute("UPDATE assemblies SET body = ? WHERE user_id = ? AND status = 0", (acc_id, user_id,))

    def update_cooler(self, user_id, acc_id):
        with self.connection:
            self.cursor.execute("UPDATE assemblies SET cooler = ? WHERE user_id = ? AND status = 0", (acc_id, user_id,))

    def update_drive(self, user_id, acc_id):
        with self.connection:
            self.cursor.execute("UPDATE assemblies SET drive = ? WHERE user_id = ? AND status = 0", (acc_id, user_id,))

    def update_motherboard(self, user_id, acc_id):
        with self.connection:
            self.cursor.execute("UPDATE assemblies SET motherboard = ? WHERE user_id = ? AND status = 0", (acc_id, user_id,))

    def update_psu(self, user_id, acc_id):
        with self.connection:
            self.cursor.execute("UPDATE assemblies SET psu = ? WHERE user_id = ? AND status = 0", (acc_id, user_id,))

    def update_ram(self, user_id, acc_id):
        with self.connection:
            self.cursor.execute("UPDATE assemblies SET ram = ? WHERE user_id = ? AND status = 0", (acc_id, user_id,))

    def update_video_card(self, user_id, acc_id):
        with self.connection:
            self.cursor.execute("UPDATE assemblies SET video_card = ? WHERE user_id = ? AND status = 0", (acc_id, user_id,))

    def update_status(self, user_id, name):
        with self.connection:
            self.cursor.execute("UPDATE assemblies SET status = 1, name = ? WHERE user_id = ? AND status = 0", (name, user_id,))

    # Получение последнего несобранного пк.
    def get_info_pc(self, user_id=None, build_id=None, status=0):
        accessories = self.cursor.execute('''
        SELECT body.name, cooler.name, drive.name, motherboard.name, processor.name, psu.name, ram.name, video_card.name, 
        SUM(body.price+cooler.price+drive.price+motherboard.price+processor.price+psu.price+ram.price+video_card.price) 
        FROM assemblies
        JOIN body
            ON assemblies.body = body.id
        JOIN cooler
            ON assemblies.cooler = cooler.id
        JOIN drive
            ON assemblies.drive = drive.id
        JOIN motherboard
            ON assemblies.motherboard = motherboard.id
        JOIN processor
            ON assemblies.processor = processor.id
        JOIN psu
            ON assemblies.psu = psu.id
        JOIN ram
            ON assemblies.ram = ram.id
        JOIN video_card
            ON assemblies.video_card = video_card.id
        WHERE (user_id = ? OR assemblies.id =?) AND assemblies.status = ?
        ''', (user_id, build_id, status, )).fetchone()
        return accessories

    # Получение последнего несобранного пк.
    def get_not_accessoriess(self, build_id):
        accessories = self.cursor.execute('SELECT body, cooler, drive, motherboard, processor, psu, ram, video_card FROM assemblies WHERE id = ? ', (build_id,)).fetchone()
        return accessories

    def get_all_id_accessoriesss(self, build_id):
        accessories = self.cursor.execute('SELECT body, cooler, drive, motherboard, processor, psu, ram, video_card FROM all_assemblies WHERE id = ? ', (build_id,)).fetchone()
        return accessories

    def get_all_accessories(self, build_id=None):
        accessories = self.cursor.execute('''
        SELECT body.name, cooler.name, drive.name, motherboard.name, processor.name, psu.name, ram.name, video_card.name, 
        SUM(body.price+cooler.price+drive.price+motherboard.price+processor.price+psu.price+ram.price+video_card.price) 
        FROM all_assemblies
        JOIN body
            ON all_assemblies.body = body.id
        JOIN cooler
            ON all_assemblies.cooler = cooler.id
        JOIN drive
            ON all_assemblies.drive = drive.id
        JOIN motherboard
            ON all_assemblies.motherboard = motherboard.id
        JOIN processor
            ON all_assemblies.processor = processor.id
        JOIN psu
            ON all_assemblies.psu = psu.id
        JOIN ram
            ON all_assemblies.ram = ram.id
        JOIN video_card
            ON all_assemblies.video_card = video_card.id
        WHERE all_assemblies.id = ?
        ''', (build_id, )).fetchone()
        return accessories