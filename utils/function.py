from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import UserDataBase
from utils import CallBackData

user_db = UserDataBase()

# Обновление комплектующих
def update_accessories(name, user_id, acc_id):
    if name == "body":
        user_db.update_body(user_id, acc_id)
    elif name == "cooler":
        user_db.update_cooler(user_id, acc_id)
    elif name == "drive":
        user_db.update_drive(user_id, acc_id)
    elif name == "motherboard":
        user_db.update_motherboard(user_id, acc_id)
    elif name == "processor":
        user_db.update_processor(user_id, acc_id)
    elif name == "psu":
        user_db.update_psu(user_id, acc_id)
    elif name == "ram":
        user_db.update_ram(user_id, acc_id)
    elif name == "video_card":
        user_db.update_video_card(user_id, acc_id)

# Комплектующие
def get_accessories(name, user_id):
    if name == "body":
        res = user_db.get_body()
    elif name == "cooler":
        res = user_db.get_cooler()
    elif name == "drive":
        res = user_db.get_drive()
    elif name == "motherboard":
        res = user_db.get_motherboard(user_id=user_id)
    elif name == "processor":
        res = user_db.get_processor(user_id=user_id)
    elif name == "psu":
        res = user_db.get_psu(user_id)
    elif name == "ram":
        res = user_db.get_ram()
    elif name == "video_card":
        res = user_db.get_video_card()
    markups = InlineKeyboardMarkup()
    for i in res:
        markups.add(InlineKeyboardButton(text=i[1], callback_data=CallBackData.accessories.new(type="accessories", name=name, id=i[0])))
    markups.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="assembling_pc"))
    return markups

# Описание комплектующих
def get_description_accessories(name, acc_id):
    if name == "body":
        res = user_db.get_info_body(acc_id)
    elif name == "cooler":
        res = user_db.get_info_cooler(acc_id)
    elif name == "drive":
        res = user_db.get_info_drive(acc_id)
    elif name == "motherboard":
        res = user_db.get_info_motherboard(acc_id)
    elif name == "processor":
        res = user_db.get_info_processor(acc_id)
    elif name == "psu":
        res = user_db.get_info_psu(acc_id)
    elif name == "ram":
        res = user_db.get_info_ram(acc_id)
    elif name == "video_card":
        res = user_db.get_info_video_card(acc_id)
    return res



