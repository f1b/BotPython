from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

def StartKeybord():
    keybord = InlineKeyboardMarkup()

    button_1 = InlineKeyboardButton(text = 'ПМИ', callback_data='ПМИ')
    button_2 = InlineKeyboardButton(text = 'ФИИТ', callback_data='ФИИТ')
    
    return keybord.add(button_1).add(button_2)


def Level():
    keybord = InlineKeyboardMarkup()

    button_1 = InlineKeyboardButton(text = '1 курс', callback_data='1-курс')
    button_2 = InlineKeyboardButton(text = '2 курс', callback_data='2-курс')
    button_3 = InlineKeyboardButton(text = '3 курс', callback_data='3-курс')
    button_4 = InlineKeyboardButton(text = '4 курс', callback_data='4-курс')
    
    return keybord.add(button_1).add(button_2).add(button_3).add(button_4)

def StandartKeybord():
    keybord = InlineKeyboardMarkup()

    button_1 = InlineKeyboardButton(text = 'Получить список доступных книги', callback_data='books')
    button_2 = InlineKeyboardButton(text = 'Изменить данные о себе', callback_data='change')
    
    return keybord.add(button_1).add(button_2)

def AdminKeybord():
    keybord = InlineKeyboardMarkup()

    button_1 = InlineKeyboardButton(text = 'Получить список доступных книги', callback_data='books')
    button_2 = InlineKeyboardButton(text = 'Изменить данные о себе', callback_data='change')
    button_3 = InlineKeyboardButton(text = 'Добавить книгу', callback_data='addbook')
    button_4 = InlineKeyboardButton(text = 'Удалить книгу', callback_data='delbook')
    button_5 = InlineKeyboardButton(text = 'Добавить админа', callback_data='addadmin')
    button_6 = InlineKeyboardButton(text = 'Удалить админа', callback_data='deladmin')
    button_7 = InlineKeyboardButton(text = 'Изменить данные о книге', callback_data='changeflags')
    
    return keybord.add(button_1).add(button_2).add(button_3).add(button_4).add(button_5).add(button_6).add(button_7)