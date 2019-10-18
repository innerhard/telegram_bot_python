# Функция проверки доступа Usera к данным
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
    con.close()


# def current_User_Autorize():

# update.message.reply_text(
#       f'Привет  {update.message.chat.id}, Я бот \n' +
#       f'я умею выполнять команды:')
#  for arr_to_str in bigdata.bot_set_config:
#     update.message.reply_text(
#        f'{arr_to_str} - {bigdata.bot_set_config[arr_to_str]}')
