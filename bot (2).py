import asyncio
import logging
from aiogram import Bot, types
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InputMediaPhoto, InputMediaVideo, ChatActions
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.utils.emoji import emojize
from aiogram.types import InputFile
from contextlib import suppress
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,MessageToDeleteNotFound)
from config import TOKEN
import sqlite3
import string
import time
import random
from datetime import datetime

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

registration=InlineKeyboardMarkup(row_width=4).add(InlineKeyboardButton('Зарегистрироваться❤️', callback_data='reg'))

msk = KeyboardButton('Москва')
smr = KeyboardButton('Самара')
nn = KeyboardButton('Нижний Новгород')
hab = KeyboardButton('Хабаровск')
rnd = KeyboardButton('Ростов-на-Дону')
spb = KeyboardButton('Санкт-Петербург')
citys = ReplyKeyboardMarkup(resize_keyboard=True).row(msk, smr, nn).row(hab, rnd, spb)

kandidat=InlineKeyboardButton('Ввести ключ кандидата🔑', callback_data='kandidat')
sotrudnik=InlineKeyboardButton('Ввести ключ сотрудника🔑', callback_data='sotrudnik')
status=InlineKeyboardMarkup(row_width=2).add(kandidat).add(sotrudnik)

state=InlineKeyboardButton('Выбрать свой статус✅', callback_data='state')
alls=InlineKeyboardButton('Общая информация📖', callback_data='alls')
hr=InlineKeyboardButton('Вопросы в HR❓', callback_data='hr')
karier=InlineKeyboardButton('Карьера и развитие в компании📈', callback_data='karier')
menu=InlineKeyboardMarkup(row_width=2).add(state).add(alls).add(hr).add(karier)

return_menu=InlineKeyboardMarkup(row_width=4).add(InlineKeyboardButton('Вернуться в Меню↩️', callback_data='return_menu'))

okompany=InlineKeyboardButton('🔴О компании🔴', callback_data='okompany')
kmlive=InlineKeyboardButton('🟠Как мы живем🟠', callback_data='kmlive')
ofis=InlineKeyboardButton('🟡Офисы🟡', callback_data='ofis')
day=InlineKeyboardButton('🟢Рабочий день🟢', callback_data='day')
dress_kod=InlineKeyboardButton('🔵Дресс-код🔵', callback_data='dress_kod')
contacts=InlineKeyboardButton('🟣Соцсети и контакты🟣', callback_data='contacts')
ob_all=InlineKeyboardMarkup(row_width=2).add(okompany).add(kmlive).add(ofis).add(day).add(dress_kod).add(contacts)
ob_user=InlineKeyboardMarkup(row_width=2).add(okompany).add(ofis).add(contacts)

trud=InlineKeyboardButton('1️⃣Трудоустройство и оформление', callback_data='trud')
adapt=InlineKeyboardButton('2️⃣Адаптация', callback_data='adapt')
otpusk=InlineKeyboardButton('3️⃣Отпуск', callback_data='otpusk')
sickleave=InlineKeyboardButton('4️⃣Больничный', callback_data='sickleave')
dayoff=InlineKeyboardButton('5️⃣Day off', callback_data='dayoff')
money=InlineKeyboardButton('6️⃣Деньги', callback_data='money')
skidka=InlineKeyboardButton('7️⃣Партнерские скидки', callback_data='skidka')
dms=InlineKeyboardButton('8️⃣ДМС', callback_data='dms')
hr_all=InlineKeyboardMarkup(row_width=2).add(trud).add(adapt).add(otpusk).add(sickleave).add(dayoff).add(money).add(skidka).add(dms)
hr_kandidate=InlineKeyboardMarkup(row_width=2).add(trud).add(adapt)

referal=InlineKeyboardButton('Реферальная программа (приведи друга)🤝', callback_data='referal')
vuz=InlineKeyboardButton('Работа с ВУЗами и практика👥', callback_data='vuz')
education=InlineKeyboardButton('Обучение👨‍🎓', callback_data='education')
ipr=InlineKeyboardButton('ИПР🪜', callback_data='ipr')
karier_all=InlineKeyboardMarkup(row_width=2).add(referal).add(vuz).add(education).add(ipr)

Facebook=InlineKeyboardButton('Facebook🌐', url='https://www.facebook.com/RostelecomSolar')
Instagram=InlineKeyboardButton('Instagram🌐', url='https://www.instagram.com/rostelecom_solar')
Youtube=InlineKeyboardButton('Youtube🌐', url='https://www.youtube.com/c/RTSolar')
Vkontakte=InlineKeyboardButton('Vkontakte🌐', url='https://vk.com/workinsecurity')
contact=InlineKeyboardMarkup(row_width=2).add(Facebook,Instagram,Youtube,Vkontakte)


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()

class Photo(StatesGroup):
        photo=State()

class Reg(StatesGroup):
        name=State()
        city=State()
        number=State()

class Key(StatesGroup):
        key=State()
        key1=State()

start_edit=0
@dp.message_handler(commands=['start'])
async def process_start_command(msg: types.Message):
    global start_edit
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    if msg.from_user.last_name == None:
        name=str(msg.from_user.first_name)
    elif msg.from_user.first_name == None:
        name=str(msg.from_user.last_name)
    else:
        name=str(msg.from_user.first_name+" "+msg.from_user.last_name)
    i = [j[0] for j in c.execute("SELECT id FROM User")] 
    if msg.from_user.id not in i: start_edit = await bot.send_photo(msg.from_user.id, "AgACAgIAAxkBAAMJYUd2nz4RvzY-vbqwGFzlIZN4hZ8AAiC8MRtmnThKqbpqAnId9ogBAAMCAAN4AAMgBA",caption = "<b>Привет </b>"+name+"!👋\n\nЯ бот компании <b>Ростелеком-Солар</b>, который поможет тебе лучше узнать о нас и наших возможностях.\n\nПрежде чем знакомиться с компанией, давай пройдем маленькую регистрацию...\n\nНажни на кнопку ниже👇",reply_markup=registration, parse_mode='HTML')
    else: await msg.answer("Ты уже проходил регистрацию, если возникли вопросы по работе бота введи команду /menu")
    c.close()
    db.close()
    

@dp.callback_query_handler(lambda c: c.data == 'reg', state="*")
async def process_callback_reg(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.last_name == None:
        name=str(callback_query.from_user.first_name)
    elif callback_query.from_user.first_name == None:
        name=str(callback_query.from_user.last_name)
    else:
        name=str(callback_query.from_user.first_name+" "+callback_query.from_user.last_name)
    global start_edit
    asyncio.create_task(delete_message(start_edit, 0))
    await bot.send_photo(callback_query.from_user.id, "AgACAgIAAxkBAAMJYUd2nz4RvzY-vbqwGFzlIZN4hZ8AAiC8MRtmnThKqbpqAnId9ogBAAMCAAN4AAMgBA",caption = "<b>Привет </b>"+name+"!👋\n\nЯ бот компании <b>Ростелеком-Солар</b>, который поможет тебе лучше узнать о нас и наших возможностях.\n\nПрежде чем знакомиться с компанией, давай пройдем маленькую регистрацию...\n\nНажни на кнопку ниже👇",parse_mode='HTML')
    await bot.send_message(callback_query.from_user.id,"Как тебя зовут? (Полное ФИО)")
    await Reg.name.set()

@dp.message_handler(state=Reg.name)
async def reg_name(msg: types.Message, state: FSMContext):
    if type(msg.text)==str:
        await state.update_data(name_reg=msg.text)
        await msg.answer("Укажи из какого ты города (если твоего города нету в списке, введи сам)", reply_markup = citys)
        await Reg.city.set()
    else: 
        await msg.answer("Твое имя помоему состоит из букв, попробуй еще раз")
        return

@dp.message_handler(state=Reg.city)
async def reg_city(msg: types.Message, state: FSMContext):
    if type(msg.text)==str:
        await state.update_data(city_reg=msg.text)
        await msg.answer("Введи свой номер телефона в формате: 89...", reply_markup=types.ReplyKeyboardRemove())
        await Reg.number.set()
    else: 
        await msg.answer("Выбери свой город из списка или введи сам")
        return

@dp.message_handler(state=Reg.number)
async def reg_number(msg: types.Message, state: FSMContext):
    if type(msg.text)==str:
        await state.update_data(number_reg=msg.text)
        user_data = await state.get_data()
        db = sqlite3.connect('databot.db')
        c = db.cursor()
        c.execute('INSERT INTO User VALUES (?,?,?,?,?,?)', (msg.from_user.id,user_data['name_reg'].title(),user_data['city_reg'].title(),user_data['number_reg'],time.ctime(),"user")) 
        db.commit()
        await state.finish()
        await bot.send_photo(msg.from_user.id, "AgACAgIAAxkBAAPZYUjBH1D0Nz42nn5w0Q6yS2naIfAAAmG4MRvBVElKLSeS8J-uK78BAAMCAAN5AAMgBA", caption = "<b>Регистрация успешно завершена!</b>\n\nНиже представленно меню бота.\nТы всегда можешь его вызвать введя команду /menu",reply_markup=menu, parse_mode='HTML')
        c.close()
        db.close()
    else:
        await msg.answer("Введи свой номер телефона")
        return

menu_delete=0
@dp.message_handler(commands=['menu'])
async def process_menu_command(msg: types.Message):
    global menu_delete
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if msg.from_user.id not in i: await bot.send_message(msg.from_user.id,"ТЫ еще не прошел регистрацию!")
    else:
        menu_delete = await bot.send_photo(msg.from_user.id, "AgACAgIAAxkBAAPZYUjBH1D0Nz42nn5w0Q6yS2naIfAAAmG4MRvBVElKLSeS8J-uK78BAAMCAAN5AAMgBA", caption ="<b>Меню: </b>", reply_markup = menu, parse_mode='HTML')

state_delete=0
@dp.callback_query_handler(lambda c: c.data == 'state')
async def process_callback_state(callback_query: types.CallbackQuery):
    global menu_delete
    global state_delete
    asyncio.create_task(delete_message(menu_delete, 0)) 
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: state_delete = await bot.send_message(callback_query.from_user.id, 'Выбери статус: ', reply_markup = status)
    c.close()
    db.close()


@dp.callback_query_handler(lambda c: c.data == 'kandidat', state="*")
async def process_callback_kandidat(callback_query: types.CallbackQuery,  state: FSMContext):
    global state_delete
    asyncio.create_task(delete_message(state_delete, 0))
    await bot.send_message(callback_query.from_user.id,"Введи ключ полученный из офера")
    await Key.key.set()

@dp.message_handler(state=Key.key)
async def key(msg: types.Message, state: FSMContext):
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT k_e_y FROM key")]
    if msg.text in i:
        c.execute("""UPDATE User SET status=? WHERE id=?""",("candidate",msg.from_user.id))
        db.commit()
        c.execute('''DELETE FROM key WHERE k_e_y = ?''', (msg.text, ))
        db.commit()
        await msg.answer("Ключ успешно активирован!\nТеперь твой статус: Кандидат\nВозможности бота для тебя увеличены")
    else: await msg.answer("Неверный ключ!")
    await state.finish()
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'sotrudnik', state="*")
async def process_callback_sotrudnik(callback_query: types.CallbackQuery,  state: FSMContext):
    global state_delete
    asyncio.create_task(delete_message(state_delete, 0))
    await bot.send_message(callback_query.from_user.id,"Введи ключ полученный от руководителя")
    await Key.key1.set()

@dp.message_handler(state=Key.key1)
async def key1(msg: types.Message, state: FSMContext):
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT k_e_y FROM key")]
    if msg.text in i:
        c.execute("""UPDATE User SET status=? WHERE id=?""",("sotrudnik",msg.from_user.id))
        db.commit()
        c.execute('''DELETE FROM key WHERE k_e_y = ?''', (msg.text, ))
        db.commit()
        await msg.answer("Ключ успешно активирован!\nТеперь твой статус: Сотрудник\nВозможности бота для тебя увеличены")
    else: await msg.answer("Неверный ключ!")
    await state.finish()
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'return_menu')
async def process_callback_return_menu(callback_query: types.CallbackQuery):
    global menu_delete
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else:
        menu_delete = await bot.send_photo(callback_query.from_user.id, "AgACAgIAAxkBAAPZYUjBH1D0Nz42nn5w0Q6yS2naIfAAAmG4MRvBVElKLSeS8J-uK78BAAMCAAN5AAMgBA", caption ="<b>Меню: </b>", reply_markup = menu, parse_mode='HTML')
    c.close()
    db.close()


alls_delete=0
@dp.callback_query_handler(lambda c: c.data == 'alls')
async def process_callback_alls(callback_query: types.CallbackQuery):
    global menu_delete
    global alls_delete
    asyncio.create_task(delete_message(menu_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: 
        c.execute('SELECT status FROM User WHERE id = ?',(callback_query.from_user.id, ))
        status=c.fetchone()
        if str(*status) == "user": alls_delete = await bot.send_photo(callback_query.from_user.id, "AgACAgIAAxkBAAPqYUjD-3IAASiy46LZhqV_D9cg5dJ4AAJouDEbwVRJSolbWeNAB8bhAQADAgADeQADIAQ", caption ='Выбери подраздел: ', reply_markup = ob_user)
        else: alls_delete = await bot.send_photo(callback_query.from_user.id, "AgACAgIAAxkBAAPqYUjD-3IAASiy46LZhqV_D9cg5dJ4AAJouDEbwVRJSolbWeNAB8bhAQADAgADeQADIAQ", caption ='Выбери подраздел: ', reply_markup = ob_all)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'okompany')
async def process_callback_okompany(callback_query: types.CallbackQuery):
    global alls_delete
    asyncio.create_task(delete_message(alls_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id, "Мы появились на рынке информационной безопасности в 2015 году под названием Solar Security. Мы всегда делали ставку на доступность и удобство технологий и следовали этому принципу во всем, от проработки простых и понятных интерфейсов до обеспечения заказчикам всех возможных вариантов доставки технологий.\nКомпания стояла у истоков российского рынка сервисов ИБ, первой сформулировала концепцию «кибербезопасность как сервис», которая сегодня становится доминирующей. Этот визионерский взгляд на рынок информационной безопасности позволил нам возглавить направление рынка, создав первый в России коммерческий центр мониторинга и реагирования на киберугрозы Solar JSOC, который и спустя годы удерживает лидерские позиции в сегменте и обеспечивает безопасность государственных и коммерческих структур.\n\nВ дальнейшем направление сервисов кибербезопасности было усилено благодаря выводу на рынок платформы Solar MSS, которая делает технологии защиты от киберугроз доступными, в том числе, компаниям малого и среднего бизнеса.\nМы создавали компанию, которая сможет занять лидирующее положение на рынке информационной безопасности, и понимали, что для этого необходимо развитие собственных технологий - более эффективных и удобных, чем существующие на рынке решения. Следуя этой стратегии, мы разработали первую российскую систему для контроля коммуникаций и борьбы с утечками данных Solar Dozor, шлюз веб-безопасности Solar webProxy, первое в мире решение для проверки безопасности исходного кода со встроенными технологиями декомпиляции и деобфускации Solar appScreener, а также первую российскую IGA-платформу для управления правами доступа Solar inRights.\nСегодня компания является ведущим игроком на рынке системной интеграции, реализуя масштабные комплексные проекты по информационной безопасности, в том числе в области обеспечения соответствия требованиям регуляторов и защиты АСУ ТП.\n\nВ мае 2018 года «Ростелеком» приобрел 100% акций Solar Security, чтобы создать на ее базе национального оператора сервисов кибербезопасности. Новая компания названа «Ростелеком-Солар». Теперь направление кибербезопасности «Ростелекома» реализует уже кластер компаний, отвечающих за сервисы, разработку технологий и интеграционные решения по защите от киберугроз.\n\nКак системообразующий игрок, мы ставим своей целью развитие отрасли и технологий информационной безопасности, а также противодействие кибератакам на всех уровнях – от стратегически значимых национальных проектов до защиты бизнеса и повышения киберграмотности населения.", reply_markup = return_menu, parse_mode='HTML')
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'kmlive')
async def process_callback_kmlive(callback_query: types.CallbackQuery):
    global alls_delete
    asyncio.create_task(delete_message(alls_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'Мы любим учиться, веселиться и ЗОЖ.\nПроводим внутренние митапы, делимся знаниями друг с другом, учимся на внешних курсах и в корпоративном университете.\nМы молоды и любим движение. Занимаемся йогой, проводим утренние зарядки, играем в футбол, волейбол и видеоигры.\nА еще мы обожаем праздники и отмечаем не только Новый год и День рождения компании, но ещё Хэллоуин, 14 февраля и даже середину лета (отличный повод для общего тимбилдинга).', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'ofis')
async def process_callback_ofis(callback_query: types.CallbackQuery):
    global alls_delete
    asyncio.create_task(delete_message(alls_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'<b>Москва:</b> на Вятской: м. Савеловская, ул. Вятская 35/4, БЦ «Вятка», 1-й подъезд.\n\n<b>Москва:</b> на Никитском: м. Охотный ряд, Никитский пер., д. 7, стр. 1.\n\n<b>Самара:</b> Молодогвардейская 204, Бизнес-Центр «Бэл-Плаза», 9 этаж.\n\n<b>Хабаровск:</b> ул. Серышева, д.56, 3 этаж.\n\n<b>Нижний Новгород:</b> Казанское Шоссе 25 к.2, 4й этаж.\n\n<b>Ростов-на-Дону</b> пер. Доломановский, 70 Д.\n\n<b>Санкт-Петербург:</b> Синопская набережная, 14.', reply_markup = return_menu, parse_mode='HTML')
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'day')
async def process_callback_day(callback_query: types.CallbackQuery):
    global alls_delete
    asyncio.create_task(delete_message(alls_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'Рабочий день в компании начинается в 10.00, а заканчивается в 18.30. Обеденный перерыв 30 минут с период с 12.00 до 15.00. Но мы гибкие, свой личный график всегда можно обсудить с руководителем.', reply_markup = return_menu, parse_mode='HTML')
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'dress_kod')
async def process_callback_dress_kod(callback_query: types.CallbackQuery):
    global alls_delete
    asyncio.create_task(delete_message(alls_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'В офисе придерживаемся Smart Casual.К клиенту ходим всегда в деловом\nНе очень любим экстремальные луки, шорты и шлёпанцы в летнее время года', reply_markup = return_menu, parse_mode='HTML')
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'contacts')
async def process_callback_contacts(callback_query: types.CallbackQuery):
    global alls_delete
    asyncio.create_task(delete_message(alls_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'Facebook: Официальная страница. Тут мы рассказываем новости о нашем бизнесе.\n\nInstagram: тут балуемся stories с мероприятий и из жизни офисов.\n\nYoutube: Сюда выкладываем полезные ролики о продуктах и сервисах, вебинары и прошедшие трансляции.\n\nVkontakte: Здесь контент для молодых специалистов.', reply_markup = contact, parse_mode='HTML')
    c.close()
    db.close()

hr_delete=0
@dp.callback_query_handler(lambda c: c.data == 'hr')
async def process_callback_hr(callback_query: types.CallbackQuery):
    global menu_delete
    global hr_delete
    asyncio.create_task(delete_message(menu_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: 
        c.execute('SELECT status FROM User WHERE id = ?',(callback_query.from_user.id, ))
        status=c.fetchone()
        if str(*status) == "user": await bot.send_message(callback_query.from_user.id, "Данный раздел доступен только для участников со статусом Кандидат или Сотрудник!", reply_markup = return_menu)
        elif str(*status) == "candidate": hr_delete = await bot.send_photo(callback_query.from_user.id, "AgACAgIAAxkBAAIBWGFI80pI4bdN2kwZ5o7SYL0xAZsaAAKruDEbwVRJSmx8xypKdbQYAQADAgADeQADIAQ", caption ='Выбери подраздел: ', reply_markup = hr_kandidate)
        else: hr_delete = await bot.send_photo(callback_query.from_user.id, "AgACAgIAAxkBAAIBWGFI80pI4bdN2kwZ5o7SYL0xAZsaAAKruDEbwVRJSmx8xypKdbQYAQADAgADeQADIAQ", caption ='Выбери подраздел: ', reply_markup = hr_all)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'trud')
async def process_callback_trud(callback_query: types.CallbackQuery):
    global hr_delete
    asyncio.create_task(delete_message(hr_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'До оформления ознакомься с обязательными инструктажами по охране труда, пожарной безопасности и внутренними нормативными документами нашей компании.\n\nСОЛАР_ЛНА для ознакомления (https://cloud.solarsecurity.ru/s/aADmGw9BLXnSs38/authenticate/showShare)\nпароль qPdCB~5R\n\nДля подготовки комплекта документов для приема в компанию  нам потребуются сканы или фотокопии документов (п. 1-9) из перечня ниже. Документы необходимо направить за 5 рабочих дня, в виде вложений или ссылкой на папку GoogleDocs или Яндекс.Диск на OK-RTK-SOLAR@rt-solar.ru (отдел кадров). В теме письма укажи: ФИО_Документы для оформления.\n\n1. Паспорт (все заполненные страницы)\n2. Страховое свидетельство Государственного пенсионного страхования РФ\n3. ИНН (свидетельство о постановке на учет в налоговом органе) https://service.nalog.ru/inn.do\n4. Документ об образовании (диплом, если нет диплома – аттестат)\n5. Копия трудовой книжки (если ТК ведётся в электронном виде)\n6. Военный билет (ВСЕ ЗАПОЛНЕННЫЕ СТРАНИЦЫ)\n7. Свидетельство о рождении детей (несовершеннолетних)\n8. Загранпаспорт (если есть, необходима для оформления банковской карты)\n9. Фото в корпоративном стиле (нейтральный фон, без излишеств) в электронном виде для пропуска\n10. Действующие сертификаты и дипломы дополнительного образования\n\nОригиналы документов, которые нужно будет передать в офис (дополнительно сориентируем, как это сделать через курьера, если потребуется):\n1. Трудовая книжка\n2. Справка по форме 182н – для расчета больничных листов\n3. Справка о доходах за 2021 год 2-НДФЛ\n\nДля оформления в Москве: ждем тебя в офисе к 10-00 по адресу: Никитский пер. 7с1., 1 этаж\n\nКак нас найти: Проходите здание Центрального телеграфа, между 7 домом и 7с1 лестница наверх, поднимаетесь по ней, там вход, на проходной необходимо получить пропуск (с собой иметь паспорт).\n\nПосле получения пропуска позвоните, я Вас встречу.\nВот мой номер в 8(977) 487-45-17, если возникнут вопросы, обращайся)', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'adapt')
async def process_callback_adapt(callback_query: types.CallbackQuery):
    global hr_delete
    asyncio.create_task(delete_message(hr_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'Как ты уже видел в оффере, испытательный срок в Соларе составляет 3 месяца. Но мы понимаем, что адаптация на новом месте работы иногда занимает больше времени, поэтому мы подготовили целую программу мероприятий, которые помогут тебе быстрее познакомиться с компанией, руководителем и командой, вовлечься в работу, чувствовать себя комфортно и показывать отличные результаты. Тебя жду welcome-курс, welcome-встреча, экскурсия по офису, регулярные встречи с руководителем и наставником, дистанционные курсы и еще много инетересного, о чем ты узнаешь в первые дни.', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'otpusk')
async def process_callback_otpusk(callback_query: types.CallbackQuery):
    global hr_delete
    asyncio.create_task(delete_message(hr_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'У нас есть график отпусков и мы стараемся его придерживаться.\nОформляется отпуск с помощью заявки на портале за две недели до начала и согласовывается с руководителем. Узнать сколько дней отпуска накопилось можно у себя в профиле на портале. Если остались вопросы пиши на OK-RTK-SOLAR@rt-solar.ru', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'sickleave')
async def process_callback_sickleave(callback_query: types.CallbackQuery):
    global hr_delete
    asyncio.create_task(delete_message(hr_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'Если ты заболел и взял больничный, пиши на OK-RTK-SOLAR@rt-solar.ru с темой письма «Отсутствие».\n\nТы выздоровел и закрыл больничный:\n1.  Если больничный бумажный, отправь скан на OK-RTK-SOLAR@rt-solar.ru и следом обязательно принеси или отправь через секретарей оригинал.\n2.  Если у тебя электронный больничный, пришли данные электронного больничного на OK-RTK-SOLAR@rt-solar.ru и всё. Эти данные работник может получить у лечащего врача или и в личном кабинете на сайте ФСС.', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'dayoff')
async def process_callback_dayoff(callback_query: types.CallbackQuery):
    global hr_delete
    asyncio.create_task(delete_message(hr_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'Ты с самого утра чувствуешь себя нехорошо, тебе срочно надо посетить врача, резко заболел твой питомец или затопили соседи – в нашей жизни случается много непредвиденных обстоятельств. Для таких случаев у нас есть day off, но тебе придется согласовать его с руководителем. В этот день ты остаешься на связи, но у ноутбука можешь не присутствовать. Однако будь готов к срочным вопросам в What’s Up.\n\nУ нас есть несколько правил, которые надо учесть, ознакомься заранее:\nDay Off – это не дополнительный отпуск\nDay Off нельзя брать на 3 дня подряд\nDay Off нельзя брать в одновременно пятницу и следующий за ней понедельник (два подряд рабочих дня)\nDay Off не предоставляется после оплаченных в двойном размере рабочих выходных\nDay Off нельзя присоединять к праздничным дням\n\nНеобходимо установить автоответ в почте и по возможности быть на связи по экстренным вопросам', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'money')
async def process_callback_money(callback_query: types.CallbackQuery):
    global hr_delete
    asyncio.create_task(delete_message(hr_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'Заработная плата:\nВыплачивается 8-го и 23-го числа каждого месяца. 23-го числа за первые дне недели текущего месяца и 8-го числа за оставшиеся две.\nРазмер твоей первой выплаты зависит от даты твоего приема. Не пугайся, если первая выплата будет небольшой – уже со следующей все стабилизируется.\n\nМатериальная помощь:\nЖизнь – штука непредсказуемая и хорошие вещи случаются также часто, как и плохие. Мы хотим помочь тебе в трудную минуту или сделать счастливый период еще ярче – для этого у нас предусмотрена материальная помощь. Материальная помощь – однократная выплата по личному заявлению сотрудника, которая выплачивается в размере до 50 00 рублей в случаях:\n•   регистрации брака, рождения или усыновления ребенка\n•   смерти супруга, родителей, детей, усыновителей или усыновленных, опекунов\nДля ее получения тебе нужно всего лишь собрать небольшой пакет документов и подписать заявление – обращайся в Отдел кадрового администрирования, тебя там проконсультируют.\n\nПремии:\nКаждый из нас вносит свой неповторимый вклад в работу компании. Мы это очень ценим, поэтому используем несколько систем премирования, какая для тебя – будет указано в твоем оффере. Для получения выплаты тебе нужно выполнить все свои ключевые показатели эффективности или КПЭ. КПЭ — это числовые показатели деятельности, которые помогают измерить степень достижения целей или оптимальности процесса, а именно: результативность и эффективность. Свои личные показатели и более подробную информацию сможешь спросить у руководителя или HR BP.', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'skidka')
async def process_callback_skidka(callback_query: types.CallbackQuery):
    global hr_delete
    asyncio.create_task(delete_message(hr_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'На нашем корпоративном портале есть раздел, который поможет тебе сохранить свой бюджет – раздел корпоративных скидок. Специальные цены на абонементы фитнес-клубов, школы английского языка, дома отдыха, билеты в театр, занятия на скалодромах, скидки у туроператоров и многое другое как и в Москве, так и в других регионах. Также мы всегда открыты к новым предложениям и попытаемся раздобыть скидку исходя из твоих пожеланий, нужно только написать на почту (benefits@rt-solar.ru).', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'dms')
async def process_callback_dms(callback_query: types.CallbackQuery):
    global hr_delete
    asyncio.create_task(delete_message(hr_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'Хорошее самочувствие – залог высокой продуктивности и креативных проектов. После успешного прохождения испытательного срока в течение 2х недель ты будешь подключен к программе добровольного медицинского страхования (или кратко - ДМС).  По программе ДМС можно обратиться за медицинской помощью в платное лечебное учреждение, вызвать из платной клиники врача на дом или скорую помощь, сдать необходимые анализы, посетить стоматолога или воспользоваться телемедициной не выходя из дома и получить консультацию врача онлайн. Хочешь, чтобы такая помощь могла быть оказана всем членам твоей семьи? Не вопрос, подключай своих родственников к ДМС по корпоративным ценам.', reply_markup = return_menu)
    c.close()
    db.close()

karier_delete=0
@dp.callback_query_handler(lambda c: c.data == 'karier')
async def process_callback_karier(callback_query: types.CallbackQuery):
    global menu_delete
    global karier_delete
    asyncio.create_task(delete_message(menu_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: 
        c.execute('SELECT status FROM User WHERE id = ?',(callback_query.from_user.id, ))
        status=c.fetchone()
        if str(*status) == "sotrudnik": karier_delete = await bot.send_photo(callback_query.from_user.id, "AgACAgIAAxkBAAIBlGFI-5OVBUE29tEjleXuTcQOn4xCAAKyuDEbwVRJSut240jh9Fr1AQADAgADeQADIAQ", caption ='Выбери подраздел: ', reply_markup = karier_all)
        else: await bot.send_message(callback_query.from_user.id, "Данный раздел доступен только для участников со статусом Сотрудник!", reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'referal')
async def process_callback_referal(callback_query: types.CallbackQuery):
    global karier_delete
    asyncio.create_task(delete_message(karier_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'В компании действует внутренняя реферальная программа. Сотрудники могут рекомендовать своих друзей на открытые вакансии компании и, когда рекомендованый сотрудник пройдет испытательный срок, рекомендатель получает денежный бонус.', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'vuz')
async def process_callback_vuz(callback_query: types.CallbackQuery):
    global karier_delete
    asyncio.create_task(delete_message(karier_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'Наша компания активно растет и развивается. Уже сейчас ряд подразделений берут к себе на стажирвоку студентов и выпускников ВУЗов, а в ближайшее время мы будем масштабировать программу стажировок на всю компанию.', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'education')
async def process_callback_education(callback_query: types.CallbackQuery):
    global karier_delete
    asyncio.create_task(delete_message(karier_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'В компании обучение делится на внешнее и внутреннее.\n\nВнутреннее обучение проводится на учебном портале Skills: здесь ты можешь пройти более 100 электронных курсов по продуктам и услугам компании, soft-skills и управленческим навыкам. Так же на портале публикуются анонсы очных событий, на них ты сможешь записаться после прохождения испытательного срока.\n\nА еще у нас есть две электронные библиотеки: МИФ и Альпина. Подтянуть английский можно в Skyeng, для сотрудников нашей компании есть скидки.\n\nВнешнее обучение проходит на внешних учебных площадках вне компании, если тебе требуется внешне обучение, ты можешь обсудить это со своим руководителем.\n\nПодробней о возможностях обучения и развития в компании, ты можешь узнать по ссылке. Любые вопросы по обучению пиши на training@rt-solar.ru.', reply_markup = return_menu)
    c.close()
    db.close()

@dp.callback_query_handler(lambda c: c.data == 'ipr')
async def process_callback_ipr(callback_query: types.CallbackQuery):
    global karier_delete
    asyncio.create_task(delete_message(karier_delete, 0))
    db = sqlite3.connect("databot.db")
    c = db.cursor()
    i = [j[0] for j in c.execute("SELECT id FROM User")]
    if callback_query.from_user.id not in i: await bot.send_message(callback_query.from_user.id,"ТЫ еще не прошел регистрацию!")
    else: await bot.send_message(callback_query.from_user.id,'Индивидуальный план развития (ИПР)– это список действий, которые ты готов совершить для развития своих навыков и компетенций. Он создается в рамках Диалога о развитии на 3-6 месяцев. Работа над планом и развитием компетенций даст тебе возможность эффективней выполнять свои текущие задачи и расти в компании.\n\nНе старайся развивать все и сразу, действуй сфокусировано! Обсуди с руководителем 2-3 компетенции, развитие которых даст наибольший эффект для повышения твоей результативности. При создании плана помни, что в нем должно быть не только изучение теории, но и развитие через опыт коллег и через решение рабочих задач. Подробней узнать об Индивидуальном плане развития ты можешь задать своему HR BP  или написав на training@rt-solar.ru.', reply_markup = return_menu)
    c.close()
    db.close()

@dp.message_handler(commands=['photos'],state="*")
async def process_photos_command(msg: types.Message, state: FSMContext):
    await msg.answer("Отправь фото")
    await Photo.photo.set()

@dp.message_handler(content_types=['photo'],state=Photo.photo)
async def photo(msg: types.Message, state: FSMContext):
    await msg.answer(msg.photo[-1].file_id)
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)