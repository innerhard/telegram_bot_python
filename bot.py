from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import logging
import settings
import bigdata
import ephem
import random
import db_connector
import sqlite3
import sys

see_no_evil = emojize(":see_no_evil:", use_aliases=True)
logging.basicConfig(format='%(asctime)s - %(levelname)s - $(message)s',
                    level=logging.INFO, filename='bot.log')
now = datetime.datetime.now()
# Функция проверки id user возвращает либо boolean


def verificate_User(x):
    status_Verif = False
    con = None
    con = sqlite3.connect('c:/projects/ultrabot/db_current_user.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Users")
    results = cursor.fetchall()
    for user_info in results:
        if str(x) == str(user_info[6]):
            status_Verif = True
        return status_Verif
    con.close()


def greet_user(bot, update):
    text = 'Вызван /start'
    logging.info(text)
    user_id = update.message.chat.id
    result_verif_user = verificate_User(user_id)
    if verificate_User(user_id) == True:
        update.message.reply_text(
            f'Доступ разрешен {result_verif_user} у тебя есть дополнительные команды для управления группой')
        for arr_to_str in bigdata.bot_set_config:
            update.message.reply_text(
                f'{arr_to_str} - {bigdata.bot_set_config[arr_to_str]}')
    else:
        update.message.reply_text(
            f'Доступ Запрещён {result_verif_user}')


def talk_to_me(bot, update):
    user_text = update.message.text.split(" ")
    logging.info(
        f'User: {update.message.chat.username}, Chat id:' +
        f'{update.message.chat.id} Message: {update.message.text}')
    if user_text[0] == "/za300":
        update.message.reply_text(
            f"{bigdata.joke_data[random.randrange(1, int(len(bigdata.joke_data)-1), 1)]}")
    if user_text[0] == "/planet":
        if len(user_text) == 1:
            update.message.reply_text("Введите комманду типа: /planet Mars")
        elif len(user_text) > 1:
            need_planet = user_text[1]
            for _0, _1, name in ephem._libastro.builtin_planets():

                if need_planet == name:
                    cuerpo = getattr(ephem, name)
                    const = ephem.constellation(
                        cuerpo(f"{now.year}/{now.month}/{now.day}"))
                    update.message.reply_text(
                        f"Есть такая планета {need_planet} и" +
                        f" она сейчас в созвездии {const[1]}")
                    break


def main():
    newBot = Updater(settings.api_key, request_kwargs=settings.PROXY)
    logging.info('Бот запускается')
    dp = newBot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    bots_complite = CommandHandler('za300', talk_to_me)
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(bots_complite)
    planet_search = CommandHandler('planet', talk_to_me)
    dp.add_handler(planet_search)
    newBot.start_polling()
    newBot.idle()


main()
