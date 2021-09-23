import asyncio
from aiogram import Bot, types
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType
from config1 import TOKEN
import sqlite3
import string
import random
import secrets
import time


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

class Admin(StatesGroup):
    token = State()
    login=State()
    password=State()

async def generate_alphanum_crypt_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    crypt_rand_string = ''.join(secrets.choice(
        letters_and_digits) for i in range(length))
    return crypt_rand_string

@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    await msg.answer("/condidat - сгенерировать ключ для кандидата\n\n/sotrudnik - сгенерировать ключ для кандидата")

@dp.message_handler(commands=['condidat'], state="*")
async def process_condidat_command(msg: types.Message, state: FSMContext):
    await msg.answer("Введи токен:")
    await Admin.token.set()

@dp.message_handler(commands=['sotrudnik'], state="*")
async def process_condidat_command(msg: types.Message, state: FSMContext):
    await msg.answer("Введи токен:")
    await Admin.token.set()

@dp.message_handler(state=Admin.token)
async def Admin_login(msg: types.Message, state: FSMContext):
    db = sqlite3.connect("databot1.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT token FROM User")]
    if int(msg.text) in i:
        await msg.answer("Введи логин:")
        await Admin.login.set()
    else: 
        await msg.answer("Неверный токен")
        await state.finish()
    c.close()
    db.close()

@dp.message_handler(state=Admin.login)
async def Admin_login(msg: types.Message, state: FSMContext):
    db = sqlite3.connect("databot1.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT lgn FROM User")]
    if msg.text in i:
        await msg.answer("Введи пароль:")
        await Admin.password.set()
    else: 
        await msg.answer("Неверный логин")
        await state.finish()
    c.close()
    db.close()

@dp.message_handler(state=Admin.password)
async def Admin_login(msg: types.Message, state: FSMContext):
    db = sqlite3.connect("databot1.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT pswd FROM User")]
    if msg.text in i:
        key = await generate_alphanum_crypt_string(28)
        await msg.answer("Успешно пройдена аутентификация!\nТвой ключ: " + str(key))
        await state.finish()
        db1 = sqlite3.connect("databot.db")
        c1 = db1.cursor()
        c1.execute('INSERT INTO key VALUES (?,?)', (key,time.ctime())) 
        db1.commit()
        c1.close()
        db1.close()
    else: 
        await msg.answer("Неверный логин")
        await state.finish()
    c.close()
    db.close()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


