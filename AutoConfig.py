import checker as ck
import database as dt
import users
import os

try:
    os.system("pip install aiogram")
except:
    print("Не удалось установить aiogram")

try:
    os.system("pip install sqlite3")
except:
    print("Не удалось установить sqlite")

try:
    os.mkdir("books")
except Exception as ex:
    print("Ошибка: ", ex)

try:
    os.mkdir("databases")
except Exception as ex:
    print("Ошибка: ", ex)