import fileinput,os
import keybords as kb
import Logger as log
import classes
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import InputFile

token = ""

bot = Bot(token)
dp = Dispatcher(bot)

users = {}

#создать систему классов
#разобрать файл config
#создать список пользователей
#
#

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    users[str(message.from_user.id)] = classes.User(message.from_user.id)
    if(users[str(message.from_user.id)].IsInBase(message.from_user.id)):
        if(users[str(message.from_user.id)].IsAdmin()):
            await message.answer("Привет, я бот библиотекарь, созданный силами студентов ФИИТа и самого бога. ФИИТ ТОП!",reply_markup=kb.AdminKeybord())
        else:
            await message.answer("Привет, я бот библиотекарь, созданный силами студентов ФИИТа и самого бога. ФИИТ ТОП!",reply_markup=kb.StandartKeybord())
    else:
        await message.answer("Привет, я бот библиотекарь, созданный силами студентов ФИИТа и самого бога. ФИИТ ТОП! \nТеперь укажите своё направление подготовки и курс.",reply_markup=kb.StartKeybord())

@dp.callback_query_handler(lambda call:(call.data == "ПМИ") or (call.data == "ФИИТ"))
async def course(call:CallbackQuery):
    await bot.delete_message(call.from_user.id,call.message.message_id)
    users[str(call.from_user.id)].Direction(call.data)
    await bot.send_message(call.from_user.id,"Отлично, теперь выберите курс.", reply_markup=kb.Level())

@dp.callback_query_handler(lambda call:call.data in ["1-курс", "2-курс", "3-курс", "4-курс"])
async def direction(call:CallbackQuery):
    await bot.delete_message(call.from_user.id,call.message.message_id)
    users[str(call.from_user.id)].Course(call.data)
    users[str(call.from_user.id)].SaveClient()
    if(users[str(call.from_user.id)].IsAdmin()):
        await bot.send_message(call.from_user.id,"Отлично, данные сохранены.", reply_markup=kb.AdminKeybord())
    else:
        await bot.send_message(call.from_user.id,"Отлично, данные сохранены.", reply_markup=kb.StandartKeybord())
    
@dp.callback_query_handler(lambda call:call.data == "books")
async def books(call:CallbackQuery):
    await bot.delete_message(call.from_user.id,call.message.message_id)
    books = users[str(call.from_user.id)].ReturnAllBooks()
    if(len(books) > 0):  
        result = "Доступные вам книги:\n\n"      
        keybord = InlineKeyboardMarkup()
        for x in range(0,len(books)):
            result += "id книги: "+str(books[x][0])+"\nНазвание книги: "+books[x][1]+"\n\n"
            button = InlineKeyboardButton(text = books[x][1], callback_data=x)    
            keybord.add(button)
        if(users[str(call.from_user.id)].IsAdmin()):
            button_1 = InlineKeyboardButton(text = 'Получить список доступных книги', callback_data='books')
            button_2 = InlineKeyboardButton(text = 'Изменить данные о себе', callback_data='change')
            button_3 = InlineKeyboardButton(text = 'Добавить книгу', callback_data='addbook')
            button_4 = InlineKeyboardButton(text = 'Удалить книгу', callback_data='delbook')
            button_5 = InlineKeyboardButton(text = 'Добавить админа', callback_data='addadmin')
            button_6 = InlineKeyboardButton(text = 'Удалить админа', callback_data='deladmin')
            button_7 = InlineKeyboardButton(text = 'Изменить данные о книге', callback_data='changeflags')
            keybord.add(button_1).add(button_2).add(button_3).add(button_4).add(button_5).add(button_6).add(button_7)
        else:
            button_1 = InlineKeyboardButton(text = 'Получить список доступных книги', callback_data='books')
            button_2 = InlineKeyboardButton(text = 'Изменить данные о себе', callback_data='change')
            keybord.add(button_1).add(button_2)
        await bot.send_message(call.from_user.id,result,reply_markup=keybord)
    else:
        if(users[str(call.from_user.id)].IsAdmin()):
            await bot.send_message(call.from_user.id,"У вас нет доступных книг.",reply_markup=kb.AdminKeybord())
        else:
            await bot.send_message(call.from_user.id,"У вас нет доступных книг.",reply_markup=kb.StandartKeybord())
    
@dp.callback_query_handler(lambda call: call.data.isdigit() and (0 <= int(call.data) < len(users[str(call.from_user.id)].books)))
async def book(call:CallbackQuery):
    await bot.delete_message(call.from_user.id,call.message.message_id)
    book = users[str(call.from_user.id)].ReturnBook(int(call.data))
    await bot.send_document(call.from_user.id,InputFile(book[2],book[3]),caption=book[1],reply_markup=kb.StandartKeybord())

@dp.callback_query_handler(lambda call:call.data == "change")
async def change(call:CallbackQuery):
    await bot.delete_message(call.from_user.id,call.message.message_id)
    await bot.send_message(call.from_user.id,"Выберите свой курс.", reply_markup=kb.StartKeybord())

@dp.message_handler(content_types=['text','document'])
async def command(message:types.Message):
    print(message.text)
    
    if(message.text == "Добавить книгу (только для администраторов)"):
        if(ch.FindByid(str(message.from_user.id))):
            cf.get_file = True
            cf.total_file = 4
            await message.answer("Отправте файл.")
        else:
            await message.answer("У вас нет прав на это действие.")
    elif(message.text == "Удалить книгу (только для администраторов)"):
        if(ch.FindByid(str(message.from_user.id))):
            cf.del_file = True
            await message.answer("Введите название или id файла")
        else:
            await message.answer("у вас нет прав на это действие")
    elif(cf.total_file == 4):
        cf.path ="books\\"+message.document.file_name
        cf.filename = message.document.file_name
        await message.document.download("books\\"+message.document.file_name)
        await message.answer('Файл успешно сохранён. \n Теперь введите название для файла\n')
        cf.total_file -=1
    elif(cf.total_file == 3):
        cf.bookname = message.text
        await message.answer("Название для файла добавлено. Теперь введите фио авторов через пробел")
        cf.total_file -=1
    elif(cf.total_file == 2):
        cf.avtors = message.text
        await message.answer("Авторы добавлены. Теперь введите комментарий к файлу.")
        cf.total_file -=1
    elif(cf.total_file == 1):
        await message.answer(dt.AppendToTable(cf.bookname,cf.path,cf.filename,cf.avtors,message.text))
        cf.total_file = 0
        cf.get_file = False
    elif(cf.del_file):
        data = dt.FindByAvtorOrNameOrID(message.text,message.text,message.text)
        if(len(data)>0):
            os.remove(data[0][2])
            await message.answer(dt.DeleteFromTable(data[0][0]))
        else:
            await message.answer("Файл не найден.")
        cf.del_file = False  
    elif(message.text == "Добавить админа (только для администраторов)"):
        if(ch.FindByid(str(message.from_user.id))):
            await message.answer("Введите id человека, которого нужно добавить к админам.")
            cf.addadmin = True
        else:
            message.answer("У вас нет прав на это действие")
    elif(message.text == "Удалить админа (только для администраторов)"):
        if(ch.FindByid(str(message.from_user.id))):
            await message.answer("Введите id человека, которого нужно удалить из админам.")
            cf.deladmin = True
        else:
            await message.answer("У вас нет прав на это действие")
    elif(cf.addadmin):
        if(ch.AppendToTable(message.text)):
            await message.answer("Админ добавлен.")
        else:
            await message.answer("Не удалось добавить админа.")
        cf.addadmin = False
    elif(cf.deladmin):
        if(ch.DeleteFromTable(message.text)):
            await message.answer("Админ удален.")
        else:
            await message.answer("Не удалось удалить админа.")
        cf.deladmin = False
    else:
        await message.answer("Я еще тупенький бот и не знаю много, поэтому я не понимаю вашу команду.",reply_markup=kb.StandartKeybord())
        
        
@dp.callback_query_handler()
async def callback_inline(call:CallbackQuery):
    pass
    
    


if __name__ == '__main__':
    print("start")
    executor.start_polling(dp, skip_updates=True)
    Dispatcher.skip_updates(dp)
