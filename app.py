from time import sleep
from aiogram import executor
from handlers import dp


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True,)
# Этот код используется для запуска. Цикл опроса используется 
# для проверки наличия обновлений в объекте "dp" (диспетчер). 
# Для параметра skip_updates установлено значение True, 
# что означает, что любые существующие обновления будут 
# пропущены, и будут проверяться только новые обновления.