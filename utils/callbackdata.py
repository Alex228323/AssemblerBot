from aiogram.utils.callback_data import CallbackData


class CallBackData:
    name_pc = CallbackData('name_pc', 'type', 'name')
    accessories = CallbackData('accessories', 'type', 'name', 'id')
    view_build = CallbackData('view_build', 'type', 'id', 'name', 'build_id')
    viewing_assembly = CallbackData('viewing_assembly', 'type', 'id')
    accessories_accept = CallbackData('accessories_accept', 'type', 'id', 'name')
 #код определяет несколько экземпляров класса CallbackData с 
 #различными конфигурациями полей данных обратного вызова, 
 #которые затем можно использовать для создания уникальных 
 #идентификаторов встроенных кнопок клавиатуры в боте

