import database as dt 
import checker as ch
import fileinput,os
import keybords as kb
import config as cf
import Logger as log
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import InputFile

token = "1268467622:AAFhmfN9Q_HCANhqz6wQGcpieN12T957EGM"

bot = Bot(token)
dp = Dispatcher(bot)


@dp.message_handler(lambda command:"курс" in command.text)
async def send_welcome(message: types.Message):
    keybord = InlineKeyboardMarkup()

    button_1 = InlineKeyboardButton(text = 'ПМИ', callback_data='пми')
    
    keybord.add(button_1)
    await message.answer("есть", reply_markup=keybord)

@dp.message_handler(content_types=['text','document'])
#async def command(message:types.Message):
 #   markup = types.InlineKeyboardMarkup()
  #  switch_button = types.InlineKeyboardButton(text='Try',callback_data='1')
   # markup.add(switch_button)
    #print(message.text)
    #await message.answer("Я еще тупенький бот и не знаю много, поэтому я не понимаю вашу команду.",reply_markup=markup)
        
        
@dp.callback_query_handler(lambda call: "пми" in call.data)
async def callback_inline(call:CallbackQuery):
    await call.answer("yesssssss")
    # Если сообщение из чата с ботом
    print(call.data)
 #   if call.message:
  #      if call.data == "1":
   #         await call.answer("good")
    # Если сообщение из инлайн-режима
    #elif call.inline_message_id:
     #   if call.data == "t":
      #      await call.answer("nooo good")
    



print("start")
executor.start_polling(dp, skip_updates=True)
Dispatcher.skip_updates(dp)
