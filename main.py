from googletrans import Translator
import aiogram
import LanguagesDictionary as LD
import keyboard as k
from aiogram import types
import sqlite3

transl = Translator()

START = "Привет, я бот переводчик. Просто напиши мне любое слово и я переведу его ; (Для выбора языка просто напиши /choose)"
CHOOSE = "Выберите язык перевода"

bot = aiogram.Bot(token='6036112652:AAFFuxwoDQtSBP8ZJOsuMqXGQtZST9BICK4')

dp = aiogram.Dispatcher(bot)
con = sqlite3.connect('TranslatorBase.db')
print('Бот успешно запущен')


@dp.message_handler(commands=['start'])
async def process_start_command(message: aiogram.types.Message):

    mycursor = con.cursor()

    sql = "SELECT * FROM users WHERE id = ?"
    adr = (str(message.from_user.id),)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    if myresult is None or myresult == [] or myresult == ():
        mycursor = con.cursor()
        sql = "INSERT INTO users (id, lang) VALUES (?, ?)"
        val = (str(message.from_user.id), "ru")
        mycursor.execute(sql, val)
        con.commit()

    await message.reply(START)


@dp.message_handler(commands=['choose'])
async def process_start_command(message: aiogram.types.Message):
    await message.reply(CHOOSE, reply_markup=k.keyb)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback_kb1btn1(callback_query: aiogram.types.CallbackQuery):
    if callback_query.data in LD.LANGUES:

        lang = callback_query.data

        mycursor = con.cursor()
        sql = "UPDATE users SET lang = ? WHERE id = ?"
        val = (lang, str(callback_query.from_user.id))

        mycursor.execute(sql, val)
        await bot.send_message(callback_query.from_user.id, "Язык перевода поменян на: " + LD.LANGDICT[lang])

@dp.message_handler()
async def echo_message(msg: types.Message):
    mycursor = con.cursor()
    sql = "SELECT * FROM users WHERE id = ?"
    adr = (msg.from_user.id,)
    mycursor.execute(sql, adr)
    myresult = mycursor.fetchall()
    lang = myresult[0][1]
    word = transl.translate(msg.text, dest=lang).text

    await bot.send_message(msg.from_user.id, word)

if __name__ == '__main__':
    aiogram.executor.start_polling(dp)

