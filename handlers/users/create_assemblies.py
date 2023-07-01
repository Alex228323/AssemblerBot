from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from database import UserDataBase
from buttons import UserMarkups
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils import pc_text, CallBackData, update_accessories, get_description_accessories, get_accessories


class name_acc(StatesGroup):
    name = State()


user_db = UserDataBase()


# Создание новой сборки
@dp.callback_query_handler(text="create_assemblies")
async def create_assemblies(call: types.CallbackQuery):
    user_id = call.from_user.id
    res = user_db.get_user_assembling(user_id=user_id)
    if not res:#проверяет, есть ли у пользователя существующая сборка
        user_db.create_accessories(user_id=user_id)
    else:
        user_db.delete_user_assembling(res[0][0])#если это так, удаляет ее.
        user_db.create_accessories(user_id=user_id)#создание нового набора аксессуаров 
# чтобы пользователь мог снова собирать PC.
    stage = user_db.get_stage(user_id)
    data = user_db.get_info_pc(user_id=user_id)#получение этапа и информации о ПК 
    await call.message.edit_text(text=pc_text(data=data), reply_markup=UserMarkups.accessories_pc(stage))
# редактирование сообщения с текстом ПК и ответной разметкой аксессуаров ПК.

# Продолжение сборки.
@dp.callback_query_handler(text="resume_assemblies")
async def create_assemblies(call: types.CallbackQuery):
    user_id = call.from_user.id#Получает идентификатор пользователя из обратного запроса.
    stage = user_db.get_stage(user_id)  # Получение стадии сборки.
    data = user_db.get_info_pc(user_id=user_id)  # Получение данных о сборке.
    await call.message.edit_text(text=pc_text(data), reply_markup=UserMarkups.accessories_pc(stage))
# Редактирует сообщение с текстом о сборке и разметкой ответа с аксессуарами для ПК в зависимости от этапа сборки.

# Информация о сборке.
@dp.callback_query_handler(text="assembling_pc")
async def create_assemblies(call: types.CallbackQuery):
    user_id = call.from_user.id
    stage = user_db.get_stage(user_id)
    data = user_db.get_info_pc(user_id=user_id)
    await call.message.edit_text(text=pc_text(data), reply_markup=UserMarkups.accessories_pc(stage))


# Вызов поля с выборок комплектующих.
@dp.callback_query_handler(text=["processor", "body", "cooler", "drive", "motherboard", "psu", "ram", "video_card"])
async def processor(call: types.CallbackQuery):
    name, user_id = call.data, call.from_user.id    # Получение комплектующего, id пользователя.
    await call.message.edit_text("Выберите из списка", reply_markup=get_accessories(name, user_id=user_id))


@dp.callback_query_handler(CallBackData.accessories.filter(type="accessories"))
async def add_accessories(call: types.CallbackQuery, callback_data: CallBackData.accessories):
    build_id, name = callback_data["id"], callback_data["name"]     # id комплектующего, имя комплектующего
    res = get_description_accessories(name, build_id)
    await call.message.edit_text(text=f"{res[2]}\n\n<i>{res[0]}</i>\n\n<b>Стоимость:</b><code>{'{0:,}'.format(res[1]).replace(',', ' ')}₽</code>", reply_markup=UserMarkups.add_assembling(name, build_id))


# Подтверждение комплектующего.
@dp.callback_query_handler(CallBackData.accessories_accept.filter(type="accept"))
async def add_accessories(call: types.CallbackQuery, callback_data: CallBackData.accessories_accept):
    name, acc_id, user_id = callback_data['name'], callback_data['id'], call.from_user.id
    user_db.update_stage(user_id)   # Обновление статуса сборки +1.
    stage = user_db.get_stage(user_id)  # Получение стадии сборки.
    update_accessories(name, user_id, acc_id)   # Обновление комплектующего.
    data = user_db.get_info_pc(user_id=user_id)     # Получение данных о сборке.
    await call.message.edit_text(text=pc_text(data), reply_markup=UserMarkups.accessories_pc(stage))


# Ввод название сборки
@dp.callback_query_handler(text="save_assembling")
async def save_assembling(call: types.CallbackQuery):
    await call.message.edit_text("Для сохранения сборки введите название (max длина - 15 символов)")
    await name_acc.name.set()


# Сохранение сборки
@dp.message_handler(state=[name_acc.name])
async def add_accessories(message: types.Message, state: FSMContext):
    answer = message.text
    if len(answer) > 15:
        await message.answer("Вы ввели больше 15 букв, напишите еще раз")
    else:
        user_id = message.from_user.id
        user_db.update_status(user_id=user_id, name=answer)
        await message.answer(text=f'Сборка <i>{answer}</i> успешно добавлена.\nСоздайте новую сборку или посмотрите готовые решения', reply_markup=UserMarkups.main_menu(user_id))
        await state.finish()
