import sys
from os import path

from telebot import types

sys.path.append(path.join(path.dirname(__file__), '..'))

from database import db_aa as db


def keyboard(chat_data):
    database = db.Data(chat_data)
    table_list = database.get_question()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = question_1(table_list)
    itembtn2 = question_2(table_list)
    itembtn3 = question_3(table_list)
    itembtn4 = question_4(table_list)
    itembtn5 = question_5(table_list)
    itembtn6 = question_6(table_list)
    itembtn7 = question_7(table_list)
    itembtn8 = question_8(table_list)
    markup.add(itembtn1, itembtn2)
    markup.add(itembtn3, itembtn4)
    markup.add(itembtn5, itembtn6)
    markup.add(itembtn7, itembtn8)
    return markup


def question_1(list):
    if (list[0] == False):
        itembtn1 = types.KeyboardButton('Задание 1')
    else:
        itembtn1 = types.KeyboardButton('Задание 1 ✅✅')
    return itembtn1


def question_2(list):
    if (list[1] == False):
        itembtn2 = types.KeyboardButton('Задание 2')
    else:
        itembtn2 = types.KeyboardButton('Задание 2 ✅✅')
    return itembtn2


def question_3(list):
    if (list[2] == False):
        itembtn3 = types.KeyboardButton('Задание 3')
    else:
        itembtn3 = types.KeyboardButton('Задание 3 ✅✅')
    return itembtn3


def question_4(list):
    if (list[3] == False):
        itembtn4 = types.KeyboardButton('Задание 4')
    else:
        itembtn4 = types.KeyboardButton('Задание 4 ✅✅')
    return itembtn4


def question_5(list):
    if (list[4] == False):
        itembtn5 = types.KeyboardButton('Задание 5')
    else:
        itembtn5 = types.KeyboardButton('Задание 5 ✅✅')
    return itembtn5


def question_6(list):
    if (list[5] == False):
        itembtn6 = types.KeyboardButton('Задание 6')
    else:
        itembtn6 = types.KeyboardButton('Задание 6 ✅✅')
    return itembtn6


def question_7(list):
    if (list[6] == False):
        itembtn7 = types.KeyboardButton('Задание 7')
    else:
        itembtn7 = types.KeyboardButton('Задание 7 ✅✅')
    return itembtn7


def question_8(list):
    if (list[7] == False):
        itembtn8 = types.KeyboardButton('Задание 8')
    else:
        itembtn8 = types.KeyboardButton('Задание 8 ✅✅')
    return itembtn8

def question_9(list):
    if (list[7] == False):
        itembtn9 = types.KeyboardButton('Задание 8')
    else:
        itembtn9 = types.KeyboardButton('Задание 8 ✅✅')
    return itembtn9


def export():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Экспорт данных')
    markup.add(itembtn1)
    return markup
