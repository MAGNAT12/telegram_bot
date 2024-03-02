import telebot
import sqlite3
bot = telebot.TeleBot('6515489274:AAHF78K0FpDWjuaWI8LlTNJl-51Z5vHaCjg')


@bot.message_handler(commands=['start'])
def start(message):
    ness = f'Здраствуйте, <b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id, ness, parse_mode='html')
    connect = sqlite3.connect('telebot.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
        id INTEGER PRIMARY KEY, name TEXT)""")
    connect.commit()
    people_id = message.chat.id
    people_name = message.from_user.first_name
    cursor.execute(f"SELECT `id`, `name` FROM `login_id` WHERE `id` = {people_id} AND `name` = '{people_name}' ")
    data = cursor.fetchone()
    if data is None:
        user_name = message.from_user.first_name
        user_id = message.chat.id
        user_id_str = str(user_id)
        cursor.execute("INSERT INTO login_id(id, name) VALUES(?, ?);", (user_id_str, user_name))
        connect.commit()
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированны")


@bot.message_handler()
def get_user_text(message):
    if message.text == "Hello":
        bot.send_message(message.chat.id, "Привет", parse_mode='html')
    elif message.text == "id":
        bot.send_message(message.chat.id, f"Твой ID: {message.from_user.id}", parse_mode='html')
    elif message.text == "photo":
        photo = open('pn.png', 'rb')
        bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю", parse_mode='html')


bot.polling()
