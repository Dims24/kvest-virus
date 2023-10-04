import os
import random

import telebot
from datetime import datetime, timedelta
import time
from telebot import types
import json
import re

from telebot.types import InputFile

import keyboard.main_keyboard as keyboard
import database.db_aa as db
from Export.export import export_data

bot = telebot.TeleBot('6359049037:AAHP4syCStXg6ZMnL0hF7MmrB83jxc6qcso')

correct_answers = ['_Отличная работа!_', '_Попадание прямо в цель!_', '_Здорово, молодец!_',
                   '_Прекрасно справляетесь!_']

incorrect = ['_Хм.. даю ещё шанс_ 😊',
             '_Предлагаю поразмыслить ещё_',
             '_Нуууу... не то, увы_',
             '_Так-так-так, почти! Но нет!_',
             '_Давай-давай! Я в тебя верю!_',
             ]


def timeppp(message):
    newTimeString = datetime.fromtimestamp(message).strftime('%H:%M:%S - %d %b %Z')
    print(newTimeString)


def text_check(text):
    import re
    regex = re.compile('[^a-zA-Zа-яА-Я0-9]')
    return regex.sub('', text)


menedjer = 703608663
# admin_id = '64783167'
# admin_id = '703608663'
admin_id = '314051707'


# 703608663
# 64783167

# -------------Старт---------------------------
@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        if (message.from_user.id == menedjer):
            bot.send_message(message.chat.id, 'Вам доступен экспорт', reply_markup=keyboard.export())
            # bot.register_next_step_handler(message, rules)
        else:
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKbk5lGdRVqH3U0u8sIaxz7J8UgxkiawACZg8AAlGwsEiUHH3OCPuZqTAE")
            bot.send_message(message.chat.id, '_Приветствую, друзья, впереди миссия по спасению планеты, '
                                              'но для начала давайте познакомимся._\n'
                                              '\n'
                                              "_Введите название вашей команды, но перед ним обязательно поставьте !: (пример:_ *!Название*)\n"
                             , parse_mode="Markdown", reply_markup=None)
            bot.register_next_step_handler(message, rules)
    except Exception as error:
        print(f'handle_start: {error}')
        # bot.send_message(64783167, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')
        # bot.send_message(1248171558, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')
        # bot.send_message(483241197, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')


@bot.message_handler(func=lambda message: message.text.lower() == 'экспорт данных', content_types=['text'])
def export(message):
    try:
        if (message.from_user.id == menedjer):
            excel_name = export_data()
            print(excel_name)
            bot.send_document(message.chat.id, InputFile(excel_name))
            os.remove(excel_name)
    except Exception as error:
        print(f'export: {error}')


@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'animation', 'voice', 'sticker'])
def take(message):
    print(message)
    bot.delete_message(message.chat.id, message.message_id)


# -------------Правила---------------------------
def rules(message):
    try:
        if message.content_type == 'text' and message.text[:1] == '!':
            info = db.Data(message.chat)
            info.create(message.text)
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKblBlGdRyqh9RVv5OcXMBzvuZMJWTJQACGxMAAlqS2EhjB6Z1XtCrlzAE")
            bot.send_message(message.chat.id,
                             "_Отличное название. Теперь немного расскажу о правилах пользования ботом:_\n"
                             "\n"
                             "1. 1.	Бот реагирует только на сообщения, которые начинаются с ! (Пример: !ответ). "
                             "Вы можете писать в чате что угодно, но бот ответит только после сообщения с !\n"
                             "2. Ведущий в начале каждой «Ночи» будет говорить кодовое слово, которое вам необходимо "
                             "будет ввести в чате\n"
                             "3. После кодового слова у вас будет ровно 15 минут, чтобы выполнить 3 задания для "
                             "спасения планеты. Через 15 минут ответы перестанут приниматься.\n"
                             "4. Лучше будет, если вводить ответы будет 1 человек. У всех остальных на телефонах "
                             "также будет видно все, что происходит в чатах.\n"
                             "5. В игре будет 3 кодовых слова и 9 заданий в боте\n"
                             "6. В случае возникновения вопросов по взаимодействию с ботом можно обратиться к "
                             "лаборантам, ведущему или написать модератору [@blacklist_event](@blacklist_event)\n"
                             "\n"
                             "_Если все понятно введите_ *!Погнали* _и получите карту локаций. Они пригодятся "
                             "вам во время игрового дня._\n"
                             , parse_mode="Markdown")
            bot.register_next_step_handler(message, map1)
        else:
            bot.register_next_step_handler(message, rules)
    except Exception as error:
        print(f'rules: {error}')
        bot.register_next_step_handler(message, rules)


# -------------Карта 1---------------------------
def map1(message):
    try:
        if message.content_type == 'text' and message.text[:1] == '!':
            if message.text.lower() in ['!погнали']:
                bot.send_photo(message.chat.id,
                               "AgACAgIAAxkBAAICxGUceSBxAwABFvH8iAvDxCJtiOa1pAACl9AxG25C4Egy8kQCEknpowEAAwIAA3kAAzAE"
                               )
                bot.register_next_step_handler(message, entrance1)
            else:
                bot.send_message(message.chat.id, '_Введите_ *!погнали*\n'
                                 , parse_mode="Markdown")
                bot.register_next_step_handler(message, map1)
        else:
            bot.register_next_step_handler(message, map1)
    except Exception as error:
        print(f'keybor: {error}')
        bot.register_next_step_handler(message, map1)


# -------------Вход 1---------------------------
def entrance1(message):
    try:
        if message.content_type == 'text' and message.text[:1] == '!':
            if message.text.lower() in ['!безопасность']:
                bot.send_sticker(message.chat.id,
                                 "CAACAgIAAxkBAAEKblJlGdSN-UHEvZ5EdzZEn6YTjnwEtQACYw4AAgtaoEg7Cb-9icYZzTAE")
                bot.send_message(message.chat.id, "_Справа снизу есть кнопка, которая откроет меню, нажмите её "
                                                  "и выбирайте задание для спасения планеты!_\n",
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard1(message.chat))
                start_question_at(message.chat, 'entrance1')
            else:
                bot.send_message(message.chat.id, '_Неверное кодовое слово_\n'
                                 , parse_mode="Markdown")
                bot.register_next_step_handler(message, entrance1)
        else:
            bot.register_next_step_handler(message, entrance1)
    except Exception as error:
        print(f'entrance1: {error}')
        bot.register_next_step_handler(message, entrance1)


# -------------задание 1*---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'задание 1', content_types=['text'])
def question_1(message):
    try:
        if check_end_time(message.chat, 'entrance1'):
            markup = telebot.types.ReplyKeyboardRemove()
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKblJlGdSN-UHEvZ5EdzZEn6YTjnwEtQACYw4AAgtaoEg7Cb-9icYZzTAE")
            bot.send_message(message.chat.id,
                             '_Кажется, я знаю, где появился вирус! Его создал тот самый безумный ученый, '
                             'который живет со мной по соседству! Он редко выходил из квартиры, а курьеры '
                             'постоянно ему таскали какие-то заказы с химикатами. Я пробрался к нему в комнату '
                             'и сделал фотографию его рабочего места. Надо понять кто он, чем пользовался, '
                             'создавая вирус._\n'
                             '\n'
                             'Ответы пишите в любом порядке, в формате: *!Ответ*', parse_mode="Markdown",
                             reply_markup=markup)
            bot.send_photo(message.chat.id,
                           'AgACAgIAAx0CZNgM2QADmWUbG40B6JmU7ZIAAaV-xohAtTW06gACgswxG2Ir4EghTuAQ0OKyeQEAAwIAA3kAAzAE')
            bot.send_photo(message.chat.id,
                           'AgACAgIAAx0CZNgM2QADmmUbG6WCrwLKzAwc2D33csaK3_lxAAKDzDEbYivgSAyqMUW4dZ2iAQADAgADeQADMAQ')
            bot.register_next_step_handler(message, question_1_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_1: {error}')
        bot.register_next_step_handler(message, question_1)


def question_1_end(message):
    try:
        if check_end_time(message.chat, 'entrance1'):
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ['!лоперамид']:
                    if check_answer(message.chat, 'question_answer_1', "answer_1"):
                        bot.send_message(message.chat.id,
                                         '_Не не не, лоперамид уже был_',
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, question_1_end)
                    else:
                        change_answer(message.chat, 'question_answer_1', "answer_1")
                        if check_answer_final(message.chat, 'question_answer_1'):
                            final_question_1(message)
                        else:
                            bot.send_message(message.chat.id,
                                             "_Верно, осталось немного._",
                                             parse_mode="Markdown")
                            bot.register_next_step_handler(message, question_1_end)
                elif message.text.lower() in ['!стрептомицин']:
                    if check_answer(message.chat, 'question_answer_1', "answer_2"):
                        bot.send_message(message.chat.id,
                                         '_Верно, но подобный ответ уже засчитан_',
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, question_1_end)
                    else:
                        change_answer(message.chat, 'question_answer_1', "answer_2")
                        if check_answer_final(message.chat, 'question_answer_1'):
                            final_question_1(message)
                        else:
                            bot.send_message(message.chat.id,
                                             "_Верно, осталось немного._",
                                             parse_mode="Markdown")
                            bot.register_next_step_handler(message, question_1_end)
                elif message.text.lower() in ['!он уволен',
                                              '!уволен',
                                              '!его уволили',
                                              '!уволили']:
                    if check_answer(message.chat, 'question_answer_1', "answer_3"):
                        bot.send_message(message.chat.id,
                                         '_Уже известно, что он уволен_',
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, question_1_end)
                    else:
                        change_answer(message.chat, 'question_answer_1', "answer_3")
                        if check_answer_final(message.chat, 'question_answer_1'):
                            final_question_1(message)
                        else:
                            bot.send_message(message.chat.id,
                                             "_Верно, осталось немного._",
                                             parse_mode="Markdown")
                            bot.register_next_step_handler(message, question_1_end)
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, random.choice(incorrect), parse_mode="Markdown")
                    bot.register_next_step_handler(message, question_1_end)
            else:
                bot.register_next_step_handler(message, question_1_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_1_end: {error}')
        bot.register_next_step_handler(message, question_1_end)


def final_question_1(message):
    change(message.chat, "question_1")
    if check_final(message.chat, 1):
        map_virus(message, True)
    else:
        bot.send_message(message.chat.id,
                         '_Отличный результат! Можете выбрать следующее задание, или готовиться к началу дня._',
                         parse_mode="Markdown", reply_markup=keyboard.keyboard1(message.chat))


# -------------задание 2*---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'задание 2', content_types=['text'])
def question_2(message):
    try:
        if check_end_time(message.chat, 'entrance1'):
            markup = telebot.types.ReplyKeyboardRemove()
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKblhlGdTr3dDdyJULGEB0WO28ZDb66QACcg8AAiRaoEiI1kAytRS9zjAE")
            bot.send_message(message.chat.id,
                             '_Посмотрите! Что это? Какое-то зашифрованное послание. Может это ключ к тому,'
                             ' как распространяется вирус?_\n'
                             '\n'
                             'Ответ пишите в формате: *!Ответ*', parse_mode="Markdown", reply_markup=markup)
            bot.send_audio(message.chat.id,
                           'CQACAgIAAxkBAAIE4mUdvdPsGQWNmLPmL1wqFu6kHh9aAAI4NAACbp_wSG9uk8ev5uMgMAQ')
            bot.register_next_step_handler(message, question_2_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_2: {error}')
        bot.register_next_step_handler(message, question_2)


def question_2_end(message):
    try:
        if check_end_time(message.chat, 'entrance1'):
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ["!кислород", "!o2", "!о2"]:
                    change(message.chat, "question_2")
                    if check_final(message.chat, 1):
                        map_virus(message, True)
                    else:
                        bot.send_message(message.chat.id,
                                         '_Отличный результат! Можете выбрать следующее задание, или готовиться '
                                         'к началу дня._'
                                         , parse_mode="Markdown", reply_markup=keyboard.keyboard1(message.chat))
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, random.choice(incorrect),
                                     parse_mode="Markdown")
                    bot.register_next_step_handler(message, question_2_end)
            else:
                bot.register_next_step_handler(message, question_2_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_2_end: {error}')
        bot.register_next_step_handler(message, question_2_end)


# -------------задание 3---------------------------

@bot.message_handler(func=lambda message: message.text.lower() == 'задание 3', content_types=['text'])
def question_3(message):
    try:
        if check_end_time(message.chat, 'entrance1'):
            markup = telebot.types.ReplyKeyboardRemove()
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKblplGdUGFTsIE3Q-1OKY2du7cnIEfwACWg4AAsQNmUiGtb3-255fDTAE")
            bot.send_message(message.chat.id,
                             '_Сейчас вам предстоит выяснить насколько давно происходит распространение вируса. '
                             'Похоже, именно на этом калькуляторе проводили расчеты, даже записку с ними оставили. '
                             'Воспользуйтесь запиской и определите срок заражения планеты._\n'
                             '\n'
                             'Ответ пишите в формате: *!Ответ*', parse_mode="Markdown", reply_markup=markup)
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAMOZRsnuV0F9x_VOb1f8yPGB6GevBAAAsPKMRuYE9hIowF1e2rbhO0BAAMCAAN5AAMwBA')
            bot.register_next_step_handler(message, question_3_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_3: {error}')
        bot.register_next_step_handler(message, question_3)


def question_3_end(message):
    try:
        if check_end_time(message.chat, 'entrance1'):
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ["!три квартала", "!триквартала", "!3 квартала", "!3квартала"]:
                    change(message.chat, "question_3")
                    if check_final(message.chat, 1):
                        map_virus(message, True)
                    else:
                        bot.send_message(message.chat.id,
                                         '_Отличный результат! Похоже, вирус распространяется уже 9 месяцев, '
                                         'это поможет в спасении планеты. Можете выбрать следующее задание или '
                                         'готовиться к началу дня._'
                                         , parse_mode="Markdown", reply_markup=keyboard.keyboard1(message.chat))
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, random.choice(incorrect),
                                     parse_mode="Markdown")
                    bot.register_next_step_handler(message, question_3_end)
            else:
                bot.register_next_step_handler(message, question_3_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_3_end: {error}')
        bot.register_next_step_handler(message, question_3_end)


# -------------Вход 2---------------------------

@bot.message_handler(func=lambda message: message.text.lower() == '!изоляция', content_types=['text'])
def entrance2(message):
    try:
        if check_final(message.chat, 2):
            bot.send_message(message.chat.id, '_Вы проходили данный блок, введите кодовое слово, '
                                              'которое назвал ведущий _\n', parse_mode="Markdown")
        else:
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ['!изоляция']:
                    bot.send_sticker(message.chat.id,
                                     "CAACAgIAAxkBAAEKblxlGdUewRG6zqFeFZax9SYN23YWKQACaA0AArShoUgeWJn3yocDQTAE")
                    bot.send_message(message.chat.id, "_Справа снизу есть кнопка, которая откроет меню, нажмите "
                                                      "её и выбирайте задание для спасения планеты!_\n",
                                     parse_mode="Markdown", reply_markup=keyboard.keyboard2(message.chat))
                    start_question_at(message.chat, 'entrance2')
                else:
                    bot.send_message(message.chat.id, '_Неверное кодовое слово_\n'
                                     , parse_mode="Markdown")
                    bot.register_next_step_handler(message, entrance2)
            else:
                bot.register_next_step_handler(message, entrance2)
    except Exception as error:
        print(f'entrance2: {error}')
        bot.register_next_step_handler(message, entrance2)


# -------------задание 4---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'задание 4', content_types=['text'])
def question_4(message):
    try:
        if check_end_time(message.chat, 'entrance2'):
            markup = telebot.types.ReplyKeyboardRemove()
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKca5lHHJs6ylyf2Bc8EuRz4XWn1Bi2QACYw4AAgtaoEg7Cb-9icYZzTAE")
            bot.send_message(message.chat.id,
                             '_Химия – помощник любого ученого, разрабатывающего лекарства. А смешение цветов – '
                             'простейшая химия. Кажется, этот химик разрабатывал антидот для болезней желудка, '
                             'но что тут написано? Может, вам даже чем-то поможет цвет его блокнота._\n'
                             '\n'
                             'Ответ пишите в формате: *!Ответ*', parse_mode="Markdown", reply_markup=markup)
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAMPZRsyzFk271jf-zpzfMkVj6BxEQYAAtLKMRuYE9hIOVA7c0qVMzMBAAMCAAN5AAMwBA')
            bot.register_next_step_handler(message, question_4_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_4: {error}')
        bot.register_next_step_handler(message, question_4)


def question_4_end(message):
    try:
        if check_end_time(message.chat, 'entrance2'):
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ["!грелин"]:
                    change(message.chat, "question_4")
                    if check_final(message.chat, 2):
                        map_virus(message, True)
                    else:
                        bot.send_message(message.chat.id,
                                         '_Отличный результат! Возможно именно этот гормон поможет создать '
                                         'лекарство. Можете выбрать следующее задание или готовиться к началу дня._'
                                         , parse_mode="Markdown", reply_markup=keyboard.keyboard2(message.chat))
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, random.choice(incorrect),
                                     parse_mode="Markdown")
                    bot.register_next_step_handler(message, question_4_end)
            else:
                bot.register_next_step_handler(message, question_4_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_4_end: {error}')
        bot.register_next_step_handler(message, question_4_end)


# -------------задание 5---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'задание 5', content_types=['text'])
def question_5(message):
    try:
        if check_end_time(message.chat, 'entrance2'):
            markup = telebot.types.ReplyKeyboardRemove()
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKcHZlGzJbXZujDo1EpShuaDl2E8f-cwACrQ4AAuR6QUt_BjUr8hmSxjAE")
            bot.send_message(message.chat.id,
                             '_Похоже, наши исследователи нашли старую хижину, в которой проводились '
                             'какие-то эксперименты над животными. Изучите ее и ответьте на вопросы, это '
                             'должно помочь в победе над болезнью._\n'
                             '\n'
                             'Перейдите по ссылке. Ответ пишите в формате: *!Ответ*', parse_mode="Markdown",
                             reply_markup=markup)
            bot.send_message(message.chat.id, 'https://tinyurl.com/ydb9qczv', disable_web_page_preview=True)
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAICVWUcckoJ_RAeIyOYsUUNL8u-B2YEAAJ40DEbbkLgSDCi5MWh3Bw6AQADAgADeQADMAQ')
            bot.register_next_step_handler(message, question_5_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_5: {error}')
        bot.register_next_step_handler(message, question_5)


def question_5_end(message):
    try:
        if check_end_time(message.chat, 'entrance2'):
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ['!пингвин', '!пингвина']:
                    if check_answer(message.chat, 'question_answer_2', "answer_1"):
                        bot.send_message(message.chat.id,
                                         '_Не не не, пингвин уже был_',
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, question_5_end)
                    else:
                        change_answer(message.chat, 'question_answer_2', "answer_1")
                        if check_answer_final(message.chat, 'question_answer_2'):
                            final_question_2(message)
                        else:
                            bot.send_message(message.chat.id,
                                             "_Верно, осталось немного._",
                                             parse_mode="Markdown")
                            bot.register_next_step_handler(message, question_5_end)
                elif message.text.lower() in ["!ентер", "!энтер", "!enter","!enter at own risk"]:
                    if check_answer(message.chat, 'question_answer_2', "answer_2"):
                        bot.send_message(message.chat.id,
                                         '_Верно, но подобный ответ уже засчитан_',
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, question_5_end)
                    else:
                        change_answer(message.chat, 'question_answer_2', "answer_2")
                        if check_answer_final(message.chat, 'question_answer_2'):
                            final_question_2(message)
                        else:
                            bot.send_message(message.chat.id,
                                             "_Верно, осталось немного._",
                                             parse_mode="Markdown")
                            bot.register_next_step_handler(message, question_5_end)
                elif message.text.lower() in ["!огнетушитель", "!огнетушители"]:
                    if check_answer(message.chat, 'question_answer_2', "answer_3"):
                        bot.send_message(message.chat.id,
                                         '_Верно, но подобный ответ уже засчитан_',
                                         parse_mode="Markdown")
                        bot.register_next_step_handler(message, question_5_end)
                    else:

                        change_answer(message.chat, 'question_answer_2', "answer_3")
                        if check_answer_final(message.chat, 'question_answer_2'):
                            final_question_2(message)
                        else:
                            bot.send_message(message.chat.id,
                                             "_Верно, осталось немного._",
                                             parse_mode="Markdown")
                            bot.register_next_step_handler(message, question_5_end)
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, random.choice(incorrect), parse_mode="Markdown")
                    bot.register_next_step_handler(message, question_5_end)
            else:
                bot.register_next_step_handler(message, question_5_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_5_end: {error}')
        bot.register_next_step_handler(message, question_5_end)


def final_question_2(message):
    change(message.chat, "question_5")
    if check_final(message.chat, 2):
        map_virus(message, True)
    else:
        bot.send_message(message.chat.id,
                         '_Отличный результат! Можете выбрать следующее задание, или готовиться к началу дня._',
                         parse_mode="Markdown", reply_markup=keyboard.keyboard2(message.chat))


# -------------задание 6---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'задание 6', content_types=['text'])
def question_6(message):
    try:
        if check_end_time(message.chat, 'entrance2'):
            markup = telebot.types.ReplyKeyboardRemove()
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKbmNlGdV4jvO1gdlP7ZGQ8bLkAstpdQACxQ4AAoxEmUgDii518Wg0ezAE")
            bot.send_message(message.chat.id,
                             '_некоторые зараженные районы не могут связаться с нами оБычными способами. '
                             'но они пРидумали другой, кАк передавать нам свои сообщенИя с помощью света. '
                             'вниматеЛьно смотрите на видео и поймите, что они пытаются нам сказатЬ._\n'
                             '\n'
                             'Ответ пишите в формате: *!Ответ*', parse_mode="Markdown",
                             reply_markup=markup)
            bot.send_video(message.chat.id,
                           'BAACAgIAAxkBAAMRZRs23qZP7ny-aUxol75C4Fd6JrEAAhgzAAKYE9hIBqahMmaROqAwBA')
            bot.register_next_step_handler(message, question_6_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_6: {error}')
        bot.register_next_step_handler(message, question_6)


def question_6_end(message):
    try:
        if check_end_time(message.chat, 'entrance2'):
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ["!спасибо"]:
                    change(message.chat, "question_6")
                    if check_final(message.chat, 2):
                        map_virus(message, True)
                    else:
                        bot.send_message(message.chat.id,
                                         '_Отличный результат, похоже, этот район уже спасли, и они благодарят вас!'
                                         ' Можете выбрать следующее задание или готовиться к началу дня._'
                                         , parse_mode="Markdown", reply_markup=keyboard.keyboard2(message.chat))
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, random.choice(incorrect),
                                     parse_mode="Markdown")
                    bot.register_next_step_handler(message, question_6_end)
            else:
                bot.register_next_step_handler(message, question_6_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_6_end: {error}')
        bot.register_next_step_handler(message, question_6_end)


# -------------Вход 3---------------------------

@bot.message_handler(func=lambda message: message.text.lower() == '!антивирус', content_types=['text'])
def entrance3(message):
    try:
        if message.content_type == 'text' and message.text[:1] == '!':
            if check_final(message.chat, 3):
                bot.send_message(message.chat.id, '_Вы проходили данный блок, введите кодовое слово, '
                                                  'которое назвал ведущий _\n', parse_mode="Markdown")
            else:
                if message.text.lower() in ['!антивирус']:
                    bot.send_sticker(message.chat.id,
                                     "CAACAgIAAxkBAAEKbmdlGdWOA__HQsInmtWk_e7wd4IyBQACtA4AAgvSoEigkT622AoTTTAE")
                    bot.send_message(message.chat.id, "_Справа снизу есть кнопка, которая откроет меню, нажмите "
                                                      "её и выбирайте задание для спасения планеты!_\n",
                                     parse_mode="Markdown", reply_markup=keyboard.keyboard3(message.chat))
                    start_question_at(message.chat, 'entrance3')
                else:
                    bot.send_message(message.chat.id, '_Неверное кодовое слово_\n'
                                     , parse_mode="Markdown")
                    bot.register_next_step_handler(message, entrance3)
        else:
            bot.register_next_step_handler(message, entrance3)
    except Exception as error:
        print(f'entrance3: {error}')
        bot.register_next_step_handler(message, entrance3)


# -------------задание 7*---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'задание 7', content_types=['text'])
def question_7(message):
    try:
        if check_end_time(message.chat, 'entrance3'):
            markup = telebot.types.ReplyKeyboardRemove()
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKbmdlGdWOA__HQsInmtWk_e7wd4IyBQACtA4AAgvSoEigkT622AoTTTAE")
            bot.send_message(message.chat.id,
                             '_После болезни у многих появляются провалы в памяти, но ничего, мы готовы им помочь '
                             'по уникальной методике. Сейчас будут приходить фотографии, на которых что-то отсутствует,'
                             ' напишите что закрыто._\n'
                             '\n'
                             'Ответ пишите в формате: *!Ответ*', parse_mode="Markdown", reply_markup=markup)
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAMSZRs6QWkgbzJVYQlUAj4t0gRmxmIAAurKMRuYE9hIielVsagQW1kBAAMCAAN5AAMwBA')
            bot.register_next_step_handler(message, question_7_1)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_7: {error}')
        bot.register_next_step_handler(message, question_7)


def question_7_1(message):
    try:
        if check_end_time(message.chat, 'entrance3'):
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ["!свиток", "!золотой свиток"]:
                    if check_final(message.chat, 3):
                        map_virus(message, True)
                    else:
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAMTZRs7B3dsViXK0sK_IKzIBqRAAAHQAALsyjEbmBPYSLhl6UoAAe4RWQEAAwIAA3kAAzAE',
                                       caption='_Отличный результат!_'
                                       , parse_mode="Markdown")
                        bot.send_message(message.chat.id, "_Теперь попробуйте вспомнить что здесь._",
                                         parse_mode="Markdown")
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAMUZRs7a5fYXcOeWObKsM5shhiKffUAAu7KMRuYE9hINSEGPq0r8PMBAAMCAAN5AAMwBA')
                    bot.register_next_step_handler(message, question_7_2)
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, random.choice(incorrect),
                                     parse_mode="Markdown")
                    bot.register_next_step_handler(message, question_7_1)
            else:
                bot.register_next_step_handler(message, question_7_1)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_7_1: {error}')
        bot.register_next_step_handler(message, question_7_1)


def question_7_2(message):
    try:
        if check_end_time(message.chat, 'entrance3'):
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ["!мона лиза", "!картина мона лиза", "!джаконда",
                                            "!картинка джаконды", "!картина моны лизы"]:
                    if check_final(message.chat, 3):
                        map_virus(message, True)
                    else:
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAMWZRs771O7OqewdA0u3_ThIYdE2hwAAu_KMRuYE9hIr0ysoyPXAdUBAAMCAAN5AAMwBA',
                                       caption='_Отличный результат!_'
                                       , parse_mode="Markdown")
                        bot.send_message(message.chat.id, "_Теперь попробуйте вспомнить что здесь._",
                                         parse_mode="Markdown")
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAMXZRs8If47YHu-Wq5Zdr-I1lcORukAAvDKMRuYE9hIFHSe_ab9XFwBAAMCAAN5AAMwBA')
                    bot.register_next_step_handler(message, question_7_3)
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, random.choice(incorrect),
                                     parse_mode="Markdown")
                    bot.register_next_step_handler(message, question_7_2)
            else:
                bot.register_next_step_handler(message, question_7_2)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_7_2: {error}')
        bot.register_next_step_handler(message, question_7_2)


def question_7_3(message):
    try:
        if check_end_time(message.chat, 'entrance3'):
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ["!статуя", "!статуя иисуса", "!статуя иисусу", "!иисус", "!памятник",
                                            "!памятник иисусу", "!памятник иисуса", "!статуя христа",
                                            "!памятник христу", "!христос"]:
                    change(message.chat, "question_7")
                    if check_final(message.chat, 3):
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAICEWUcIkzz7JYTC3gAAdu1K_ZM2rToHgACus4xG25C4EhknPFmR48z7gEAAwIAA3kAAzAE',
                                       caption='_Отличный результат!_'
                                       , parse_mode="Markdown")
                        end(message, True)
                    else:
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAICEWUcIkzz7JYTC3gAAdu1K_ZM2rToHgACus4xG25C4EhknPFmR48z7gEAAwIAA3kAAzAE',
                                       caption='_Отличный результат! Можете выбрать следующее задание, или готовиться к началу дня._'
                                       , parse_mode="Markdown", reply_markup=keyboard.keyboard3(message.chat))
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, random.choice(incorrect),
                                     parse_mode="Markdown")
                    bot.register_next_step_handler(message, question_7_3)
            else:
                bot.register_next_step_handler(message, question_7_3)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_7_3: {error}')
        bot.register_next_step_handler(message, question_7_3)


# -------------задание 8*---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'задание 8', content_types=['text'])
def question_8(message):
    try:
        if check_end_time(message.chat, 'entrance3'):
            markup = telebot.types.ReplyKeyboardRemove()
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKbmtlGdXYm0HqrFgex3v6lzBXG1IJEgACyw0AAjR_oEiWR2jcYJrkpjAE")
            bot.send_message(message.chat.id,
                             '_Кажется, мы нашли разработки наших коллег по тому, как предотвратить этот вирус. '
                             'Они использовали совсем несложный способ кодирования, всего лишь нужно найти слова '
                             'в этом прямоугольнике из букв и ответить на вопрос,составленный из них. Пример того, '
                             'как слова там записаны тоже покажем._\n'
                             '\n'
                             'Ответ пишите в формате: *!Ответ*', parse_mode="Markdown", reply_markup=markup)
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIE4GUdvZXTMi-WwQR6yrGYrcGo6WiUAAKczzEbbp_wSELwc5VMnKdCAQADAgADeQADMAQ')
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIE4WUdvadOQWc_4lzLgTODasdK668XAAKezzEbbp_wSNZo2qdU4KTdAQADAgADeQADMAQ')
            bot.register_next_step_handler(message, question_8_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_8: {error}')
        bot.register_next_step_handler(message, question_8)


def question_8_end(message):
    try:
        if check_end_time(message.chat, 'entrance3'):
            if message.content_type == 'text' and message.text[:1] == '!':
                if message.text.lower() in ["!кишечная палочка", "!кишечнаяпалочка"]:
                    change(message.chat, "question_8")
                    if check_final(message.chat, 3):
                        map_virus(message, True)
                    else:
                        bot.send_message(message.chat.id,
                                         '_Отличный результат! Можете выбрать следующее задание '
                                         'или готовиться к началу дня_'
                                         , parse_mode="Markdown", reply_markup=keyboard.keyboard3(message.chat))
                else:
                    bot.send_chat_action(message.chat.id, 'typing')
                    bot.send_message(message.chat.id, random.choice(incorrect),
                                     parse_mode="Markdown")
                    bot.register_next_step_handler(message, question_8_end)
            else:
                bot.register_next_step_handler(message, question_8_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_8_end: {error}')
        bot.register_next_step_handler(message, question_8_end)


# -------------задание 9*---------------------------
photo = [
    'AgACAgIAAxkBAAMbZRs_UrnDSb6-4p9xqa-hKnL5C4kAAvXKMRuYE9hImm_eEIRlufUBAAMCAAN5AAMwBA',
    'AgACAgIAAxkBAAMcZRs_YebDtodiKA7tzGQkLk6poCgAAvbKMRuYE9hIY8TnngkYzC8BAAMCAAN5AAMwBA',
    'AgACAgIAAxkBAAMdZRs_cryQWHtJpXT62c6D47lwrUAAAvfKMRuYE9hIYpAD2a5Nx40BAAMCAAN5AAMwBA',
    'AgACAgIAAxkBAAMeZRs_fqavGwxc6F_FcaAlxMumJFYAAvjKMRuYE9hI5YygWuAF_6gBAAMCAAN5AAMwBA'
]


@bot.message_handler(func=lambda message: message.text.lower() == 'задание 9', content_types=['text'])
def question_9(message):
    print(message)
    try:
        if check_end_time(message.chat, 'entrance3'):
            markup = telebot.types.ReplyKeyboardRemove()
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKbmtlGdXYm0HqrFgex3v6lzBXG1IJEgACyw0AAjR_oEiWR2jcYJrkpjAE")
            bot.send_message(message.chat.id,
                             '_Мы хотим запомнить наших спасителей, поэтому сделайте, пожалуйста, нам фотографию'
                             ' на память, чтобы она навсегда осталась в архивах нашей планеты. Пример отправляем вам,'
                             ' постарайтесь, чтобы ваше фото было похоже, иначе не примем._\n', parse_mode="Markdown",
                             reply_markup=markup)
            bot.send_photo(message.chat.id,
                           random.choice(photo))
            bot.register_next_step_handler(message, question_9_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_9: {error}')
        bot.register_next_step_handler(message, question_9)


def question_9_end(message):
    try:
        if check_end_time(message.chat, 'entrance3'):
            if message.content_type == 'photo':
                keyboard_inline = types.InlineKeyboardMarkup()
                confirm_button = types.InlineKeyboardButton('Подтвердить', callback_data=f'confirm')
                cancel_button = types.InlineKeyboardButton('Отменить', callback_data='cancel')
                keyboard_inline.row(confirm_button, cancel_button)
                bot.send_photo(admin_id, message.photo[-1].file_id,
                               caption=f'Подтвердите отправку этой фотографии для "{message.chat.title}".\n'
                                       f'\n'
                                       f'Задание 9:\n'
                                       f'\n'
                                       f'[ {message.chat} ]\n',
                               reply_markup=keyboard_inline)

                @bot.callback_query_handler(func=lambda call: True)
                def callback_handler(call):
                    text = call.message.caption
                    match = re.search(r'\[(.*?)\]', text)
                    text = match.group(1).replace("'", "\"")
                    text_end = text.replace("None", "null")
                    value = json.loads(text_end)
                    chat = types.Chat.de_json(value)
                    if call.data == 'confirm':
                        change(chat, 'question_9')
                        bot.send_message(call.from_user.id, f'Фотография подтверждена у \"{chat.title}\"')
                        if check_final(chat, 3):
                            markup = telebot.types.ReplyKeyboardRemove()
                            bot.send_sticker(chat.id,
                                             "CAACAgIAAxkBAAEKbkxlGdO6slpcsB9jOt2Ge6m2cZVuywACaA0AArShoUgeWJn3yocDQTAE")
                            bot.send_message(chat.id,
                                             '_Мне кажется, вы остановили  распространение вируса. Поздравляю! '
                                             'Осталось лишь понять, какая команда внесла больший вклад, '
                                             'а пока отдыхайте._\n',
                                             parse_mode="Markdown", reply_markup=markup)
                        else:
                            bot.send_message(chat.id,
                                             '_Отличный результат! Можете выбрать следующее задание или готовиться'
                                             ' к началу дня_',
                                             parse_mode="Markdown",
                                             reply_markup=keyboard.keyboard3(chat))
                    elif call.data == 'cancel':
                        bot.send_message(chat.id, 'Хм.. даю ещё шанс 😊')
                        bot.send_message(call.from_user.id, f'Фотография отменена у \"{chat.title}\"')
                        data = {
                            "message_id": 1,
                            "from": {
                                "id": 703608663,
                                "is_bot": False,
                                "first_name": "Dmitriy",
                                "username": "Lis_Di",
                                "last_name": "None",
                                "language_code": "ru",
                                "can_join_groups": "None",
                                "can_read_all_group_messages": "None",
                                "supports_inline_queries": "None",
                                "is_premium": "None",
                                "added_to_attachment_menu": "None"
                            },
                            "chat": {
                                "id": chat.id,
                                "type": chat.type,
                                "title": chat.title
                            },
                            "date": 1694822792,
                            "text": "Стал"
                        }

                        json_data = json.dumps(data, indent=3, ensure_ascii=False)

                        fake_message = types.Message(message_id=1, date=1234567890, chat=chat,
                                                     from_user=message.from_user,
                                                     content_type="text", options=[], json_string=json_data)
                        print(fake_message)
                        bot.register_next_step_handler(fake_message, question_9_end)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Нужно фото\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_9_end)
        else:
            map_virus(message, False)
    except Exception as error:
        print(f'question_9_end: {error}')
        bot.register_next_step_handler(message, question_9_end)


# -------------Конец---------------------------
def end(message, flag):
    if flag:
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEKbkxlGdO6slpcsB9jOt2Ge6m2cZVuywACaA0AArShoUgeWJn3yocDQTAE")
        bot.send_message(message.chat.id, '_Мне кажется, вы остановили  распространение вируса. Поздравляю! '
                                          'Осталось лишь понять, какая команда внесла больший вклад, а пока отдыхайте._\n',
                         parse_mode="Markdown", reply_markup=markup)
    else:
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEKbkxlGdO6slpcsB9jOt2Ge6m2cZVuywACaA0AArShoUgeWJn3yocDQTAE")
        bot.send_message(message.chat.id,
                         '_Дажен не смотря на то, что время вышло вы все равно остановили  распространение вируса. Поздравляю! '
                         'Осталось лишь понять, какая команда внесла больший вклад, а пока отдыхайте._\n',
                         parse_mode="Markdown", reply_markup=markup)
    # bot.register_next_step_handler(message, end)


# -------------Карта---------------------------
def map_virus(message, flag):
    markup = telebot.types.ReplyKeyboardRemove()
    if flag:
        bot.send_message(message.chat.id, 'Вы справились со всеми заданиями, ожидайте наставлений ведущего',
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'К сожалению время вышло, ожидайте наставлений ведущего',
                         reply_markup=markup)


def start_question_at(chat_data, name_colum):
    database = db.Data(chat_data)
    database.start_entrance_at(f'start_{name_colum}')


def check_end_time(chat_data, column_name):
    column_name = f'start_{column_name}'
    database = db.Data(chat_data)
    time_start_tuple = database.check_end_time(column_name)

    # Переводим кортеж в строку в формате '%H:%M:%S'
    time_start_str = time_start_tuple.strftime('%H:%M:%S')

    # Получаем текущее время и приводим его к формату '%H:%M:%S'
    now_str = datetime.now().strftime('%H:%M:%S')

    # Преобразуем строки в объекты времени
    start_time = datetime.strptime(time_start_str, '%H:%M:%S').time()
    now = datetime.strptime(now_str, '%H:%M:%S').time()

    # Вычисляем end_time как текущее время плюс 15 минут
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=15)).time()
    # Проверяем, находится ли текущее время между start_time и end_time
    if start_time <= now <= end_time:
        return True
    else:
        return False


def change(user_data, name_colum):
    database = db.Data(user_data)
    database.replace(name_colum)


def check_final(chat_data, block=0):
    database = db.Data(chat_data)
    number = database.check_final(block)
    if all(number):
        return True
    else:
        return False


def change_answer(user_data, table_name, name_colum):
    database = db.Data(user_data)
    database.replace_answer(table_name, name_colum)


def check_answer_final(chat_data, table_name):
    database = db.Data(chat_data)
    number = database.check_answer_final(table_name)
    if all(number):
        return True
    else:
        return False


def check_answer(chat_data, table_name, name_colum):
    database = db.Data(chat_data)
    answer_bool = database.response_answer(table_name, name_colum)
    if answer_bool[0]:
        return True
    else:
        return False


def get_count(chat_data):
    database = db.Data(chat_data)
    answer = database.get_count()
    return answer


# -------------------------------------------------

while True:
    try:
        bot.polling(none_stop=True, timeout=5)
    except Exception as error:
        print(error)
        time.sleep(3)
