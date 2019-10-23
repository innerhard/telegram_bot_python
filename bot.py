from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import logging
import settings
import bigdata
import ephem
import random
import sqlite3

see_no_evil = emojize(":see_no_evil:", use_aliases=True)
logging.basicConfig(format='%(asctime)s - %(levelname)s - $(message)s',
                    level=logging.INFO, filename='bot.log')
now = datetime.datetime.now()

# Вывод заданий по неделям


def get_Faq(bot, update):
    user_text = update.message.text.split(" ")
    user_id = update.message.chat.id
    con = None
    con = sqlite3.connect('c:/projects/ultrabot/db_current_user.db')
    cursor = con.cursor()
    if verificate_User(user_id) is True and len(user_text) > 1:
        cursor.execute(
            f"SELECT * FROM Library_Data WHERE Name = '{user_text[1]}'")
        results = cursor.fetchall()
        for user_info in results:
            update.message.reply_text(
                f"{user_info[1]} {user_info[2]} {user_info[3]}")
    elif verificate_User(user_id) is True and len(user_text) == 1:
        cursor.execute(
            f"SELECT * FROM Library_Data")
        results = cursor.fetchall()
        for user_info in results:
            update.message.reply_text(
                f"Доступные темы для просмотра напиши /faq {user_info[1]}")
    con.close()


def get_Week_Lessons(number_week, status_verif, update):
    con = None
    con = sqlite3.connect('c:/projects/ultrabot/db_current_user.db')
    cursor = con.cursor()

    if status_verif is True:
        if number_week != "all":
            cursor.execute(
                f"SELECT * FROM Lessons WHERE ID_Week = {number_week}")
            update.message.reply_text(f"Материалы недели {number_week}")
        elif number_week == "all":
            cursor.execute(f"SELECT * FROM Lessons")
            update.message.reply_text(f"Весь план обучения")
        results = cursor.fetchall()
        for user_info in results:
            update.message.reply_text(
                f"{user_info[2]} {user_info[3]} {user_info[4]}")
    else:
        update.message.reply_text(
            f"У вас нет доступа! Зарегистрируйтесь /signin почта пароль")

    con.close()


# Функция отправки уроков
def push_Week_Lessons(bot, update):
    user_text = update.message.text.split(" ")
    user_id = update.message.chat.id
    result_verif_user = verificate_User(user_id)
    get_Week_Lessons(user_text[1], result_verif_user, update)

# Функция проверки id user возвращает либо boolean


def verificate_User(id_user):
    status_Verif = False
    con = None
    con = sqlite3.connect('c:/projects/ultrabot/db_current_user.db')
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Users")
    results = cursor.fetchall()
    for user_info in results:
        if str(id_user) == str(user_info[6]):
            status_Verif = True
        return status_Verif
    con.close()

# Возможность регистрировать пользователя


def register_User(enter_email_user, password_user, user_id):
    conn = sqlite3.connect('c:/projects/ultrabot/db_current_user.db')
    cursor = conn.cursor()
    sql = f"""UPDATE Users SET User_Id_Telegram
    = '{user_id}' WHERE User_Email = '{enter_email_user}'"""
    cursor.execute(sql)
    conn.commit()
    conn.close()

# Запуск бота


def greet_user(bot, update):
    text = 'Вызван /start'
    logging.info(text)
    user_id = update.message.chat.id

    if verificate_User(user_id) is True:
        update.message.reply_text(
            f'Доступ разрешен {update.message.chat.username} у тебя есть'
            ' дополнительные команды для управления группой')
        for arr_to_str in bigdata.bot_set_config:
            update.message.reply_text(
                f'{arr_to_str} - {bigdata.bot_set_config[arr_to_str]}')
    elif verificate_User(user_id) is False:
        update.message.reply_text(
            f'Доступ запрещён {update.message.chat.username} введи команду /'
            'signin email пароль чтобы зарегистрировать свой id телеграмма')

# Функция вхождения запросов


def talk_to_me(bot, update):
    user_text = update.message.text.split(" ")
    logging.info(
        f'User: {update.message.chat.username}, Chat id:' +
        f'{update.message.chat.id} Message: {update.message.text}')
    user_id = update.message.chat.id
    if user_text[0] == "/signin":
        register_User(user_text[1], user_text[2], user_id)
    if user_text[0] == "/za300":
        message_user = bigdata.joke_data[random.randrange(1,
                                                          int(len(bigdata.joke_data)-1), 1)]
        update.message.reply_text(f"{message_user}")
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

    week_lessons = CommandHandler('week', push_Week_Lessons)
    faq = CommandHandler('faq', get_Faq)
    bots_complite = CommandHandler('za300', talk_to_me)
    sign_in = CommandHandler('signin', talk_to_me)
    planet_search = CommandHandler('planet', talk_to_me)
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(bots_complite)
    dp.add_handler(faq)
    dp.add_handler(sign_in)
    dp.add_handler(week_lessons)
    dp.add_handler(planet_search)
    newBot.start_polling()
    newBot.idle()


main()
