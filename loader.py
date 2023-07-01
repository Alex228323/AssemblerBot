from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Переменная бота
bot = Bot(token="token", parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

# Cоздание диспатчера
dp = Dispatcher(bot, storage=storage)

