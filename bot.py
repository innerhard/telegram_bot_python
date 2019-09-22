from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import logging
import settings
import bigdata
import ephem
import random

see_no_evil = emojize(":see_no_evil:", use_aliases=True)
logging.basicConfig(format='%(asctime)s - %(levelname)s - $(message)s',
                    level=logging.INFO, filename='bot.log')
now = datetime.datetime.now()

def greet_user(bot, update):
    text = 'Вызван /start'
    logging.info(text)

    update.message.reply_text(
        f'Привет  {update.message.chat.first_name}, Я бот \n' +
        f'я умею выполнять команды:')
    for arr_to_str in bigdata.bot_set_config:
        update.message.reply_text(
            f'{arr_to_str} - {bigdata.bot_set_config[arr_to_str]}')


def talk_to_me(bot, update):
    user_text = update.message.text
    logging.info(
        f'User: {update.message.chat.username}, Chat id:' +
        f'{update.message.chat.id} Message: {update.message.text}')
    if user_text == "/za300":
        update.message.reply_text(
            f"{bigdata.joke_data[random.randrange(1, int(len(bigdata.joke_data)-1), 1)]}")
    if user_text == "/planet":
        mars = ephem.Moon(f'{now.year}/{now.month}/{now.day}')
        const = ephem.constellation(mars)
        update.message.reply_text(f"{const}")
        ('Aqr', 'Aquarius')


def main():
    newBot = Updater(settings.api_key, request_kwargs=settings.PROXY)
    logging.info('Бот запускается')

    dp = newBot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    fuckfuck = CommandHandler('za300', talk_to_me)
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    fuckfuck = CommandHandler('planet', talk_to_me)
    dp.add_handler(fuckfuck)
    newBot.start_polling()
    newBot.idle()


main()
