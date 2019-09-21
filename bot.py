from emoji import emojize
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings

see_no_evil = emojize(":see_no_evil:", use_aliases=True)
logging.basicConfig(format='%(asctime)s - %(levelname)s - $(message)s',
                    level=logging.INFO, filename='bot.log')
joke_data = ['1. – У меня больной должен был умереть ещё 10 лет назад, \
             но всё ещё живёт.– Ясно: если жажда к жизни у человека боль\
             шая, медицина бессильна.',
             '2. – Доктор, микстура горькая. «А Вы представьте, что пьёте \
             коньяк».– А можно я буду пить коньяк и представлять, что это \
             микстура',
             '3. – Лёгкие у Вас, товарищ, здоровые. Сколько выдуваете? – \
             1,5 литра. – Как? У Вас в карточке написано, что 4,5 литра. – \
             Так это сухого!',
             '4. Количество бесплатных медицинских услуг в России всё время \
             уменьшается. Скоро бесплатным останется только лечебное \
             голодание.', '5. – Ваня, – спрашивает жена, – Президент \
             говорит, что ЦБ действует правильно, но несколько запоздало.\
             Как это понять?– Сейчас объясню. Вот, например, ты ведёшь машину\
             и врезалась в дерево. Но потом, всё-таки, руль повернула.', '6. \
             – Девушка, у Вас найдётся закурить?– У меня найдётся не только \
             закурить, а и выпить, и закусить, и переночевать.']


def greet_user(bot, update):
    text = 'Вызван /start'
    logging.info(text)
    update.message.reply_text(
        f'Привет  {update.message.chat.first_name}, Я бот шутник \n' +
        f'Напиши рандомное число от 1 до {len(joke_data)} и я' +
        f'расскажу тебе шутку {see_no_evil}')


def talk_to_me(bot, update):
    user_text = update.message.text
    logging.info(
        f'User: {update.message.chat.username}, Chat id:' +
        f'{update.message.chat.id} Message: {update.message.text}')
    if int(user_text) > int(len(joke_data)) or int(user_text) < 0:
        update.message.reply_text(
            f'Эй {update.message.chat.first_name},' +
            f'введи правильное числов от 1 до {len(joke_data)}')
    else:
        update.message.reply_text(f'{joke_data[int(user_text) - 1]} + ')


def main():
    newBot = Updater(settings.api_key, request_kwargs=settings.PROXY)
    logging.info('Бот запускается')

    dp = newBot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    newBot.start_polling()
    newBot.idle()


main()
