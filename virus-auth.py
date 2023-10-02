import telebot
from datetime import datetime, timedelta
import time
from telebot import types
import json
import re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import keyboard.main_keyboard as keyboard
import database.db_aa as db
from Export.export import export_data

bot = telebot.TeleBot('6020607344:AAHZxhXRZXK2Em4mLqEVj63zuDEZT55JapQ')


def timeppp(message):
    newTimeString = datetime.fromtimestamp(message).strftime('%H:%M:%S - %d %b %Z')
    print(newTimeString)


def text_check(text):
    import re
    regex = re.compile('[^a-zA-Zа-яА-Я0-9]')
    return regex.sub('', text)


menedjer = 123
admin_id = '64783167'


# 703608663
# 64783167

# -------------Старт---------------------------
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEJWK5kjZlJ2sEiTMKMjs-oA8mQYG1nzgACpy0AAvJuaUjltZfIigUasC8E")
        bot.send_message(message.chat.id, 'Привет, друг!\n'
                                          '\n'
                                          "Этот бот распределит тебя в команду для дальнейшей игры. Сейчас я попрошу "
                                          "тебя написать данные, которые были указаны при регистрации на сегодняшнее "
                                          "мероприятие👇🏼", parse_mode="Markdown", reply_markup=None)
        bot.send_message(message.chat.id, 'Введите свою фамилию, как при регистрации', reply_markup=None)

        def fio(message):
            name = message.text
            bot.send_message(message.chat.id, 'Введите своё имя, как при регистрации', reply_markup=None)
            bot.register_next_step_handler(message, find, name)

        bot.register_next_step_handler(message, fio)
    except Exception as error:
        print(f'handle_start: {error}')
        # bot.send_message(64783167, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')
        # bot.send_message(1248171558, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')
        # bot.send_message(483241197, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')


def find(message, name):
    try:
        first_second_name = f'{name.lower()} {message.text.lower()}'
        url = find_group(message.chat, first_second_name)
        keyboard_admin = InlineKeyboardMarkup()

        write_button = InlineKeyboardButton("Написать", url="https://t.me/blacklist_event")

        # Добавление кнопки в клавиатуру
        keyboard_admin.add(write_button)
        if url == "Много":
            bot.send_message(message.chat.id,
                             f"Кажется в наших данных есть люди с такой же фамилией и иминем\n"
                             f"\n"
                             f"Напишите администратору, чтобы урегулировать вопрос",
                             parse_mode="Markdown",
                             reply_markup=keyboard_admin)
        elif url != None:
            keyboard = InlineKeyboardMarkup()

            join_button = InlineKeyboardButton("Вступить", url=url[0])

            # Добавление кнопки в клавиатуру
            keyboard.add(join_button)
            bot.send_message(message.chat.id,
                             "Отлично! Вот ссылка на твой командный чат 👇🏼\n"
                             "\n"
                             "Для начала игры, в вашем чате, капитану нужно ввести команду /start",
                             parse_mode="Markdown", reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Вы уверены в вводе данных? Точно такие были указаны при регистрации?\n"
                                              "\n"
                                              'Попробуйте ещё раз. Если не получится, напишите',
                             parse_mode="Markdown", reply_markup=keyboard_admin)
            bot.send_message(message.chat.id, 'Введите свою фамилию, как при регистрации', reply_markup=None)
            def fio(message):
                name = message.text
                bot.send_message(message.chat.id, 'Введите своё имя, как при регистрации', reply_markup=None)
                bot.register_next_step_handler(message, find, name)

            bot.register_next_step_handler(message, fio)
    except Exception as error:
        print(f'find: {error}')
        bot.register_next_step_handler(message, find, name)


def find_group(chat_data, first_second_name):
    database = db.Data(chat_data)
    url = database.find_group_database(first_second_name)
    return url


while True:
    try:
        bot.polling(none_stop=True, timeout=5)
    except Exception as error:
        print(error)
        time.sleep(3)
