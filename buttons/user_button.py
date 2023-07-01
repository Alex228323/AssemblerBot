from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from database import UserDataBase
from utils import CallBackData

user_db = UserDataBase()


class UserMarkups:
    def __init__(self):
        pass

    def help_button():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Написать в поддержку", url="https://t.me/I_am_a_sssnake"))
        return markup
    
    @staticmethod
    def main_menu(user_id):
        res = user_db.get_user_assembling(user_id=user_id)#Проверка есть ли у пользователя сборки
        ready = user_db.get_user_ready_assembling(user_id=user_id)#Проверка есть ли у пользователя готовые сборки
        markup = InlineKeyboardMarkup()
        if len(res) == 1:#если есть незаконченная сборка, то предложить собрать новую или продолжить
            markup.add(InlineKeyboardButton('✏️ Продолжить сборку ✏️', callback_data='resume_assemblies'))
            markup.add(InlineKeyboardButton('⚒ Создать новую сборку ⚒', callback_data='create_assemblies'))
        else:#иначе вывести кнопку чоздать сборку
            markup.add(InlineKeyboardButton('⚒ Создать сборку ⚒', callback_data='create_assemblies'))
        if len(ready) >= 1:#Если количество готовых сборок больше или равно 1 то вывести кнопку мои сборки
            markup.add(InlineKeyboardButton('📁 Мои сборки 📁', callback_data='my_assemblies'))
        markup.add(InlineKeyboardButton('🖥 Готовые решения 🖥', callback_data='ready_assemblies'))
        return markup
        
    # Меню для добавления комплектующего.
    @staticmethod
    def add_assembling(name, build_id):
        markups = InlineKeyboardMarkup(row_width=2)
        but1 = (InlineKeyboardButton(text="⬅️ Назад", callback_data=name))
        but2 = (InlineKeyboardButton(text="Добавить", callback_data=CallBackData.accessories_accept.new(type="accept", name=name, id=build_id)))
        markups.add(but1,but2)
        return markups
    # Выбрать тип готовой сборки.
    @staticmethod
    def type_assembly(name_pc: classmethod):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('🎮 Игровой 🎮', callback_data=name_pc.new(type="info_type", name="gaming")))
        markup.add(InlineKeyboardButton('📎 Офисный 📎', callback_data=name_pc.new(type="info_type", name="office")))
        markup.add(InlineKeyboardButton('🖥 Профессиональный 🖥', callback_data=name_pc.new(type="info_type", name="professional")))
        markup.add(InlineKeyboardButton('⬅️ Назад', callback_data="assembling"))
        return markup

    @staticmethod
    def accessories_pc(stage):
        markup = InlineKeyboardMarkup()
        if stage == 1:
            markup.add(InlineKeyboardButton('Процессор', callback_data="processor"))
        elif stage == 2:
            markup.add(InlineKeyboardButton('Материнская плата', callback_data="motherboard"))
        elif stage == 3:
            markup.add(InlineKeyboardButton('Видеокарта', callback_data="video_card"))
        elif stage >= 4:
            markup.add(InlineKeyboardButton('Корпус', callback_data="body"), InlineKeyboardButton('Кулер', callback_data="cooler"))
            markup.add(InlineKeyboardButton('Диск', callback_data="drive"), InlineKeyboardButton('Блок питания', callback_data="psu"))
            markup.add(InlineKeyboardButton('Оперативная память', callback_data="ram"),)
            markup.add(InlineKeyboardButton('Сохранить сборку', callback_data="save_assembling"))
        markup.add(InlineKeyboardButton('⬅️ Назад', callback_data="assembling"))
        return markup

    @staticmethod
    def info_pc(view_build: classmethod, build_id: int, data: list, button_type: str, callbackdata: str):
        a = ["Корпус", "Кулер", "Диск", "Материнская плата", "Процессор", "Блок питания", "Оперативная память", "Видеокарта"]#строки, которые будут использоваться в качестве текста для каждой кнопки
        b = ["body", "cooler", "drive", "motherboard", "processor", "psu", "ram", "video_card"]#строки, которые будут использоваться в качестве данных обратного вызова для каждой кнопки.
        markup = InlineKeyboardMarkup()
        markup_add = []
        for i in range(0, len(data)):#Цикл for выполняет итерацию по списку данных, 
            #и если значение каждого индекса больше 1, он добавляет InlineKeyboardButton в 
            #список markup_add с соответствующим текстом и данными обратного вызова 
            #из a и b соответственно.
            if int(data[i]) > 1:
                markup_add.append(InlineKeyboardButton(text=a[i], callback_data=view_build.new(type=button_type, name=b[i], id=data[i], build_id=build_id)))
            if len(markup_add) == 2:#Если в markup_add есть два элемента, он добавляет их к объекту разметки и очищает markup_add.
                markup.add(*markup_add)
                markup_add = []
        if markup_add:#если в markup_add остались какие-либо элементы, они добавляются к объекту разметки
            markup.add(*markup_add)
        markup.add(InlineKeyboardButton('⬅️ Назад', callback_data=callbackdata))
        return markup#возвращает готовый объект разметки.
