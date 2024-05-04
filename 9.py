# телеграм бот с ваирантом игра:
import telebot
from random import randint
from token_1 import token


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    ness = f'Здраствуйте, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>'
    bot.send_message(message.chat.id, ness, parse_mode='html')

@bot.message_handler(commands=['game'])
def get_user_game(message):
    bot.send_message(message.chat.id, "Привет, это игра. Я загадал число от 1 до 10, попробуйте угадать!")
    rn = randint(1, 10)
    bot.register_next_step_handler(message, check_guess, rn)


def check_guess(message, rn):
    try:
        guess = int(message.text)
        if guess < rn:
            bot.send_message(message.chat.id, "Чуть больше")
        elif guess > rn:
            bot.send_message(message.chat.id, "Чуть меньше")
        else:
            bot.send_message(message.chat.id, "Вы угадали!")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число от 1 до 10.")


@bot.message_handler()
def get_user_text(message):
    if message.text == "Hello":
        bot.send_message(message.chat.id, "Привет", parse_mode='html')
    elif message.text == "id":
        bot.send_message(message.chat.id, f"Твой ID: {message.from_user.id}", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю", parse_mode='html')


bot.polling(none_stop=True)