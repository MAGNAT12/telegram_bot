import telebot
import sqlite3
import time
bot = telebot.TeleBot('ваш токен')

chat_states = {}

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

@bot.message_handler(commands=['premium'])
def premium(message):
    chat_states[message.chat.id] = 'waiting_premium_response'
    bot.send_message(message.chat.id, "Вы хотите купить премиум? Введите 'да' или 'нет'.")

@bot.message_handler(func=lambda message: chat_states.get(message.chat.id) == 'waiting_premium_response')
def process_premium(message):
    if message.text.lower() == "да":
        chat_states[message.chat.id] = 'waiting_activation_key'
        bot.send_message(message.chat.id, "Введите ключ активации:")
    elif message.text.lower() == "нет":
        bot.send_message(message.chat.id, "Действие было отклонено")
        chat_states[message.chat.id] = None

@bot.message_handler(func=lambda message: chat_states.get(message.chat.id) == 'waiting_activation_key')
def process_activation_key(message):
    if message.text == "h5DB5RgwajZoN0K7azGX":
        bot.send_message(message.chat.id, "Премиум успешно куплен!")
    else:
        bot.send_message(message.chat.id, "Неверный ключ активации.")
    chat_states[message.chat.id] = None
    
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
