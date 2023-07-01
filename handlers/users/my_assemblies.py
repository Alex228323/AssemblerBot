from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from database import UserDataBase
from buttons import UserMarkups
from aiogram.dispatcher.filters.state import State, StatesGroup

from utils import CallBackData, pc_text, get_description_accessories


class name_acc(StatesGroup):
    name = State()


user_db = UserDataBase()


@dp.callback_query_handler(text="my_assemblies")
async def add_accessories(call: types.CallbackQuery):
    user_id = call.from_user.id #идентификатор пользователя
    res = user_db.get_user_ready_assembling(user_id=user_id) #извлекает сохранённые сборки из базы данных
    markup = InlineKeyboardMarkup()
    for i in res:
        markup.add(InlineKeyboardButton(text=i[12], callback_data=CallBackData.viewing_assembly.new(type="viewing_accessories", 
        id=i[0])), InlineKeyboardButton(text="❌", callback_data=CallBackData.viewing_assembly.new(type="delete", id=i[0])))
#Для каждой сборки он добавляет две кнопки во встроенную разметку: 
#одну для просмотра/доступа к сборке и другую для ее удаления.
    markup.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="assembling"))
    await call.message.edit_text(text="Мои сборки", reply_markup=markup)


@dp.callback_query_handler(CallBackData.viewing_assembly.filter(type="delete"))
async def add_accessories(call: types.CallbackQuery, callback_data: CallBackData.viewing_assembly):
    acc_id = callback_data["id"]
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Да✅", callback_data=CallBackData.viewing_assembly.new(type="confirm", id=acc_id)),
              InlineKeyboardButton(text="Нет❌", callback_data="my_assemblies"))
    await call.message.edit_text(text="Вы уверены, что хотите удалить сборку?", reply_markup=markup)
    
@dp.callback_query_handler(CallBackData.viewing_assembly.filter(type="confirm"))
async def add_accessories(call: types.CallbackQuery, callback_data: CallBackData.viewing_assembly):
    user_id = call.from_user.id
    res = user_db.get_user_ready_assembling(user_id=user_id)
    for i in res:
        if i[0] == callback_data["id"]:
            name = i[12]
    name = i[12]
    acc_id = callback_data["id"]
    user_db.delete_user_assembling(acc_id=acc_id)
    await call.message.edit_text(text=f"Сборка <i>{name}</i> удалена, создайте новую или воспользуйтесь готовыми решениями", reply_markup=UserMarkups.main_menu(user_id))
    
# Информация о сборке
@dp.callback_query_handler(CallBackData.viewing_assembly.filter(type="viewing_accessories"))
async def add_accessories(call: types.CallbackQuery, callback_data: CallBackData.viewing_assembly):
    build_id, user_id = callback_data["id"], call.from_user.id
    data = user_db.get_not_accessoriess(build_id=build_id)  # Получение данных о сборке.
    data_text = user_db.get_info_pc(build_id=build_id, status=1)
    await call.message.edit_text(text=pc_text(data_text), reply_markup=UserMarkups.info_pc(CallBackData.view_build, build_id, data=data, button_type="info_pc", callbackdata="my_assemblies"))


# Информация о комплектующем
@dp.callback_query_handler(CallBackData.view_build.filter(type="info_pc"))
async def add_accessories(call: types.CallbackQuery, callback_data: CallBackData.viewing_assembly):
    name, acc_id, build_id = callback_data["name"], callback_data["id"], callback_data["build_id"]  # Получение имени, ид компле, ид сборки
    markups = InlineKeyboardMarkup()
    markups.add(InlineKeyboardButton(text="⬅️ Назад", callback_data=CallBackData.viewing_assembly.new(type="viewing_accessories", id=build_id)))
    res = get_description_accessories(name, acc_id)     # Получение информации о комплектующем
    await call.message.edit_text(text=f"{res[2]}\n\n<i>{res[0]}</i>\n\n<b>Стоимость:</b><code>{'{0:,}'.format(res[1]).replace(',', ' ')}₽</code>", reply_markup=markups)