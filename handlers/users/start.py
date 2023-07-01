from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from database import UserDataBase
from buttons import UserMarkups
from aiogram.dispatcher.filters.state import State, StatesGroup
from utils import pc_text, CallBackData, update_accessories, get_description_accessories, get_accessories


class name_acc(StatesGroup):
    name = State()


user_db = UserDataBase()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if( not user_db.check_user(message.from_user.id)):
        user_db.create_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
        await message.answer("Что умеет этот бот\n\n"
                             "/assembling – сборка вашего ПК или выбор из уже готовых решений\n\n"
                             "/help – напишите нам, если увидели ошибки или баги в системе бота",)
    else:
        await message.answer("Что умеет этот бот\n\n"
                     "/assembling – сборка вашего ПК или выбор из уже готовых решений\n\n"
                     "/help – напишите нам, если увидели ошибки или баги в системе бота",)

@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await message.answer(text='Мы ответим Вам в ближайшее время', reply_markup=UserMarkups.help_button())
    
# Создание или просмотр готовых
@dp.message_handler(commands=["assembling"])
async def assemblies(message: types.Message):
    user_id = message.from_user.id
    await message.answer(text='Создайте сборку или выберете из готовых!', reply_markup=UserMarkups.main_menu(user_id))


# Создание или просмотр готовых
@dp.callback_query_handler(text="assembling")
async def assemblies(call: types.CallbackQuery):
    user_id = call.from_user.id
    await call.message.edit_text(text='Создайте сборку, которая будет радовать Вас каждый день!', reply_markup=UserMarkups.main_menu(user_id))
   
# Ответ на непонятное сообщение
@dp.message_handler(content_types=types.ContentType.ANY)
async def echo(message: types.Message):
    await message.answer("Хмм, я не могу понять Вашего сообщения 🤔")


