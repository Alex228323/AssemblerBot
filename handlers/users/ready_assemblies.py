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


# Выбор типа компьютера.
@dp.callback_query_handler(text="ready_assemblies")
async def all_assemblies(call: types.CallbackQuery):
    await call.message.edit_text("Выберите тип желаемой сборки", reply_markup=UserMarkups.type_assembly(CallBackData.name_pc))


# Меню с выводом описания
@dp.callback_query_handler(CallBackData.name_pc.filter(type="info_type"))
async def all_assemblies(call: types.CallbackQuery, callback_data: CallBackData.name_pc):
    info = {'gaming': "Игровой компьютер – это идеальное решение для тех, кто хочет персональный компьютер (ПК), предназначенный и рассчитанный по конфигурации для компьютерных игр.",
            'office': "Офисный компьютер – это недорогая, но функциональная вычислительная машина, мощности которой достаточно для решения разного рода задач: может быть обработка электронных писем, работа с программным обеспечением по типу MS Office и 1C + БД, работа с браузерами, поиск и обработка информации.",
            'professional': "Профессиональный компьютер – это компьютер для профессиональной деятельности, который отличается от геймерского тем, что при сборке делаем упор на мощность процессора и объем оперативной памяти.\nДанный вид ПК достаточно сильно расширит возможности визуализации инженерных и архитектурных проектов."}
    name = callback_data["name"]
    markups = InlineKeyboardMarkup()
    markups.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="ready_assemblies"), InlineKeyboardButton(text="Далее ➡️", callback_data=CallBackData.name_pc.new(type="view_pc", name=name)))
    markups.add()
    text = info[name]
    await call.message.edit_text(text, reply_markup=markups)


# Вывод сборок по категории
@dp.callback_query_handler(CallBackData.name_pc.filter(type="view_pc"))
async def all_assemblies(call: types.CallbackQuery, callback_data: CallBackData.name_pc):
    res = user_db.get_all_pc(callback_data["name"])
    markups = InlineKeyboardMarkup()
    for i in res:
        markups.add(InlineKeyboardButton(text=i[2], callback_data=CallBackData.viewing_assembly.new(type="ready_viewing_accessories", id=i[0])))
    markups.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="ready_assemblies"))
    await call.message.edit_text("Готовые решения ", reply_markup=markups)


@dp.callback_query_handler(CallBackData.viewing_assembly.filter(type="ready_viewing_accessories"))
async def all_assemblies(call: types.CallbackQuery, callback_data: CallBackData.viewing_assembly):
    build_id = callback_data["id"]
    data = user_db.get_all_id_accessoriesss(build_id=build_id)
    date_text = pc_text(user_db.get_all_accessories(build_id))
    await call.message.edit_text(text=date_text, reply_markup=UserMarkups.info_pc(CallBackData.view_build, build_id, data=data, button_type="ready_info_pc", callbackdata="ready_assemblies"))


# Информация о комплектующем
@dp.callback_query_handler(CallBackData.view_build.filter(type="ready_info_pc"))
async def add_accessories(call: types.CallbackQuery, callback_data: CallBackData.accessories):
    name, acc_id, build_id = callback_data["name"], callback_data["id"], callback_data["build_id"]
    markups = InlineKeyboardMarkup()
    markups.add(InlineKeyboardButton(text="⬅️ Назад", callback_data=CallBackData.viewing_assembly.new(type="ready_viewing_accessories", id=build_id)))
    res = get_description_accessories(name, acc_id)
    await call.message.edit_text(text=f"{res[2]}\n\n<i>{res[0]}</i>\n\n<b>Стоимость:</b><code>{'{0:,}'.format(res[1]).replace(',', ' ')}₽</code>", reply_markup=markups)
