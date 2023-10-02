import telebot
from datetime import datetime, timedelta
import time
from telebot import types
import json
import re

import keyboard.main_keyboard as keyboard
import database.db_aa as db
from Export.export import export_data

bot = telebot.TeleBot('6079655503:AAEP47NoV2WLdqXiCWaeE2vqr7tBZWiBpjQ')


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
        # if (message.from_user.id == menedjer):
        #     bot.send_message(message.chat.id, 'Вам доступен экспорт', reply_markup=keyboard.export())
        # else:
        info = db.Data(message.chat)
        info.create()
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEJWK5kjZlJ2sEiTMKMjs-oA8mQYG1nzgACpy0AAvJuaUjltZfIigUasC8E")
        bot.send_message(message.chat.id, '_Привет, друзья!_\n'
                                          '\n'
                                          "_Покупатели авто бывают разные. Кто-то готов сразу забирать понравившуюся "
                                          "модель, а кто-то задаёт миллион вопросов и проверяет каждую деталь прежде, "
                                          "чем принять решение. Иногда вопросы могут показаться странными или даже "
                                          "глупыми, но на что не пойдёшь ради удачной сделки?\n"
                                          "\n"
                                          "У нас тоже есть несколько вопросов и заданий про автоиндустрию. Сейчас мы "
                                          "проверим, какая из команд лучше других готова к продаже абсолютно "
                                          "любого автомобиля!\n"
                                          "Ну, и как в конце любой сделки, попросим вас сфотографироваться рядом "
                                          "с отгаданной машиной_ 🚙\n"
                                          "\n"
                                          "_Если готовы, введите_ *погнали*", parse_mode="Markdown", reply_markup=None)
        bot.register_next_step_handler(message, rules)
    except Exception as error:
        print(f'handle_start: {error}')
        # bot.send_message(64783167, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')
        # bot.send_message(1248171558, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')
        # bot.send_message(483241197, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')


# @bot.message_handler(func=lambda message: message.text.lower() == 'экспорт данных', content_types=['text'])
# def export(message):
#     try:
#         if (message.from_user.id == menedjer):
#             # excel_name = export_data()
#             # print(excel_name)
#             # bot.send_document(message.chat.id, InputFile(excel_name))
#             # os.remove(excel_name)
#     except Exception as error:
#         print(f'export: {error}')


@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'animation', 'voice', 'sticker'])
def take(message):
    print(message)
    bot.delete_message(message.chat.id, message.message_id)


# -------------Правила---------------------------
def rules(message):
    try:
        if message.text.lower() in ['погнали']:
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEJWLBkjZli92j-kQqqcFb8ymUvrjjpCgACnzUAAvm7aUjr1Moqna8mOy8E")
            bot.send_message(message.chat.id,
                             "_Прежде, чем мы начнём, расскажу об игре. Всё очень просто:\n"
                             "\n"
                             "1. Придумайте название вашей команды и напишите его в этот чат\n"
                             "\n"
                             "2. Вы играете командой, которая в этом чате. Игра продлится ровно 60 минут с "
                             "кнопки /start. Время уже идёт!\n"
                             "\n"
                             "3. Вы получите меню с 8 заданиями. Выбирайте любое и нажимайте на него. "
                             "Проходить можно в любом порядке.\n"
                             "\n"
                             "4. Я пришлю вопрос или задание, решив которое вы получите фотографию. "
                             "Её необходимо повторить, используя обозначенный автомобиль.\n"
                             "\n"
                             "5. Оценивается ваша скорость прохождения задания, командная работа и  креативность "
                             "фотографии, которую вы сделаете.\n"
                             "\n"
                             "6. Сделанную фотографию необходимо прислать сюда, в чат. После этого задание "
                             "считается полностью пройденным и возле него появится 2 галочки.\n"
                             "\n"
                             "7. После прохождения всех заданий у вас останется время изучить оставшиеся автомобили "
                             "выставки. А мы пока подведём итоги игры 🏆\n"
                             "\n"
                             "Всё понятно? Если да, введите_ *готовы*\n"
                             "_Если возникнут какие-то вопросы, пиши в поддержку:_ [@blacklist_event](@blacklist_event)\n"
                             , parse_mode="Markdown")
            bot.register_next_step_handler(message, keybor)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, '_Надо ввести_ *погнали*\n',
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, rules)
    except Exception as error:
        print(f'rules: {error}')
        bot.register_next_step_handler(message, rules)


# -------------Меню---------------------------
def keybor(message):
    try:
        if message.text.lower() in ['готовы']:
            bot.send_message(message.chat.id, "_Рад, что вы готовы ! Значит, пора начинать!\n"
                                              "\n"
                                              "Справа снизу есть кнопка, которая откроет меню, нажми её!_\n",
                             parse_mode="Markdown", reply_markup=keyboard.keyboard(message.chat))
        else:
            bot.send_message(message.chat.id, '_Введите_ *готовы*\n'
                             , parse_mode="Markdown")
            bot.register_next_step_handler(message, keybor)
    except Exception as error:
        print(f'keybor: {error}')
        bot.register_next_step_handler(message, keybor)


# -------------Вопрос 1*---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'вопрос 1', content_types=['text'])
def question_1(message):
    try:
        if check_end_time(message.chat):
            start_question_at(message.chat, 'question_1')
            bot.send_message(message.chat.id,
                             '_А вы когда-нибудь задавались вопросом: «а как бы выглядела моя машина, если бы была '
                             'трансформером?».\n'
                             '\n'
                             'Я бы задался таким вопросом, будь у меня машина и права, ну или хотя бы руки_... _но я '
                             'всего лишь бот, который даже не столь умный, как ChatGPT\n'
                             '\n'
                             'Хотя на загадки у меня ума хватает_😏', parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAANoZJANpxpH2jqIowoSWPaQr_2gXFwAAkjMMRsZVoBIZP6dil5qImkBAAMCAANzAAMvBA',
                           caption='Внимательно изучите эту картинку. Попытайтесь понять, из какого автомобиля на '
                                   'выставке трансформировался этот автобот\n'
                                   '\n'
                                   '🚙 _В ответ пришлите название этого автомобиля._', parse_mode="Markdown")
            bot.register_next_step_handler(message, question_1_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_1: {error}')
        bot.register_next_step_handler(message, question_1)


def question_1_end(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["уаз", "уазик", "уаз469", "уаз 469"]:
                bot.send_message(message.chat.id,
                                 '_Молодцы 🥳 Вот вам фотография с советской классики!_', parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIBv2SQLFkhFsnmAQjJUOyPTniy9xelAALVzDEbGVaASPH3hxQ3EpXUAQADAgADeAADLwQ',
                               caption='Какая добрая фотография! Кажется, он машет кому-то. Может, своей любимой?\n'
                                       '\n'
                                       'А у вас получится такая же? Предлагаю помахать кому-то даже все вместе)',
                               parse_mode="Markdown")
                bot.register_next_step_handler(message, question_1_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_1_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'antiquiz: {error}')
        bot.register_next_step_handler(message, question_1_end)


def question_1_photo(message):
    try:
        if check_end_time(message.chat):
            if message.content_type == 'photo':
                keyboard_inline = types.InlineKeyboardMarkup()
                confirm_button = types.InlineKeyboardButton('Подтвердить', callback_data=f'confirm')
                cancel_button = types.InlineKeyboardButton('Отменить', callback_data='cancel')
                keyboard_inline.row(confirm_button, cancel_button)
                bot.send_photo(admin_id, message.photo[-1].file_id,
                               caption=f'Подтвердите отправку этой фотографии для "{message.chat.title}".\n'
                                       f'\n'
                                       f'Задание 1 (УАЗ):\n'
                                       f'\n'
                                       f'[ {message.chat} ]\n'
                                       f'#question_1#',
                               reply_markup=keyboard_inline)

                @bot.callback_query_handler(func=lambda call: True)
                def callback_handler(call):
                    text = call.message.caption
                    match = re.search(r'\[(.*?)\]', text)
                    question = re.search(r'\#(.*?)\#', text)
                    text = match.group(1).replace("'", "\"")
                    text_end = text.replace("None", "null")
                    value = json.loads(text_end)
                    chat = types.Chat.de_json(value)
                    if call.data == 'confirm':
                        end_question_at(chat, question.group(1))
                        bot.send_message(call.from_user.id, f'Фотография подтверждена у \"{chat.title}\"')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(chat.id, 'Хм, уверен это фото оценят по достоинству.\nОткрывай меню, '
                                                  'поехали дальше 👍🏼', reply_markup=keyboard.keyboard(chat))
                        if check_final(chat):
                            end_at(chat)
                            bot.send_sticker(chat.id,
                                             'CAACAgIAAxkBAAEJWLJkjZnnq-9Z6FIKDa7Sjzjv2udGTgACaS8AAmjYaUgPYCMFmg1OtC8E')
                            bot.send_message(chat.id, 'Вау! 🥳🥳🥳\n'
                                                      '\n'
                                                      'Я в восторге от того, как хорошо вы разбираетесь в автомобилях.'
                                                      'Не каждый смог бы пройти все задания и ответить на все вопросы. '
                                                      'Ещё и ваши фотографии, аплодирую стоя.\n'
                                                      '\n'
                                                      'Скоро ведущий объявит результаты игры, а вы пока можете '
                                                      'ещё насладиться выставкой\n'
                                                      '❤️', reply_markup=None)
                    elif call.data == 'cancel':
                        bot.send_message(chat.id, 'Хм.. даю ещё шанс 😊')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(call.from_user.id, f'Фотография отменена у \"{chat.title}\"')
                        bot.register_next_step_handler(message, question_1_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_1_photo)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_1_photo: {error}')
        bot.register_next_step_handler(message, question_1_photo)


# -------------Вопрос 2*---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'вопрос 2', content_types=['text'])
def question_2(message):
    try:
        if check_end_time(message.chat):
            start_question_at(message.chat, 'question_2')
            bot.send_message(message.chat.id,
                             '_Всем нам известно множество сайтов с отзывами на что-либо. На кино, на игрушки, на '
                             'электронику, одежду и т.д. Но сталкивались ли вы в жизни с отзывами, которые ну '
                             'настолько правдиво написаны, что порой даже конкретных деталей описываемой вещи '
                             'не нужно?_\n'
                             '\n'
                             '_Нам вот удалось найти один такой_ 😱', parse_mode="Markdown", )
            bot.send_voice(message.chat.id,
                           'AwACAgQAAxkBAAICF2SQWDRq8lKX44RRfy8V9TEbYYl2AALNPwACjHeBUNTWKcX-my1TLwQ',
                           caption='Послушайте аудиосообщение\n'
                                   '\n'
                                   '🚙 _В ответ напишите, на какую машину этот отзыв._', parse_mode="Markdown")
            bot.register_next_step_handler(message, question_2_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_2: {error}')
        bot.register_next_step_handler(message, question_2)


def question_2_end(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["бугатти", "bugatti", "bugatti veyron grand sport", "бугатти вейрон",
                                        "bugatti veyron"]:
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAICHmSQYt_Bovz6JOCGA0hpXyOiYxoaAAL6zTEbGVaASP1OCBLYputUAQADAgADeQADLwQ',
                               caption='_Молодцы\n'
                                       'Эти ребята на фото выглядят как настоящая команда. Тут ходят слухи, что и вы '
                                       'коллектив хоть куда. Докажите это, повторив фото_ 🔥'
                               , parse_mode="Markdown")
                bot.register_next_step_handler(message, question_2_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_2_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_2_end: {error}')
        bot.register_next_step_handler(message, question_2_end)


def question_2_photo(message):
    try:
        if check_end_time(message.chat):
            if message.content_type == 'photo':
                keyboard_inline = types.InlineKeyboardMarkup()
                confirm_button = types.InlineKeyboardButton('Подтвердить', callback_data='confirm')
                cancel_button = types.InlineKeyboardButton('Отменить', callback_data='cancel')
                keyboard_inline.row(confirm_button, cancel_button)
                bot.send_photo(admin_id, message.photo[-1].file_id,
                               caption=f'Подтвердите отправку этой фотографии для "{message.chat.title}":\n'
                                       f'\n'
                                       f'Задание 2 (бугатти):\n'
                                       f'\n'
                                       f'[ {message.chat} ]\n'
                                       f'#question_2#',
                               reply_markup=keyboard_inline)

                @bot.callback_query_handler(func=lambda call: True)
                def callback_handler(call):
                    text = call.message.caption
                    match = re.search(r'\[(.*?)\]', text)
                    question = re.search(r'\#(.*?)\#', text)
                    text = match.group(1).replace("'", "\"")
                    text_end = text.replace("None", "null")
                    value = json.loads(text_end)
                    chat = types.Chat.de_json(value)
                    if call.data == 'confirm':
                        end_question_at(chat, question.group(1))
                        bot.send_message(call.from_user.id, f'Фотография подтверждена у \"{chat.title}\"')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(chat.id, 'Хм, уверен это фото оценят по достоинству.\n Открывай меню, '
                                                  'поехали дальше 👍🏼', reply_markup=keyboard.keyboard(chat))
                        if check_final(chat):
                            end_at(chat)
                            bot.send_sticker(chat.id,
                                             'CAACAgIAAxkBAAEJWLJkjZnnq-9Z6FIKDa7Sjzjv2udGTgACaS8AAmjYaUgPYCMFmg1OtC8E')
                            bot.send_message(chat.id, 'Вау! 🥳🥳🥳\n'
                                                      '\n'
                                                      'Я в восторге от того, как хорошо вы разбираетесь в автомобилях.'
                                                      'Не каждый смог бы пройти все задания и ответить на все вопросы. '
                                                      'Ещё и ваши фотографии, аплодирую стоя.\n'
                                                      '\n'
                                                      'Скоро ведущий объявит результаты игры, а вы пока можете '
                                                      'ещё насладиться выставкой\n'
                                                      '❤️', reply_markup=None)
                    elif call.data == 'cancel':
                        bot.send_message(chat.id, 'Хм.. даю ещё шанс 😊')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(call.from_user.id, f'Фотография отменена у \"{chat.title}\"')
                        bot.register_next_step_handler(message, question_2_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_2_photo)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_2_photo: {error}')
        bot.register_next_step_handler(message, question_2_photo)


# -------------Вопрос 3---------------------------

@bot.message_handler(func=lambda message: message.text.lower() == 'вопрос 3', content_types=['text'])
def question_3(message):
    try:
        if check_end_time(message.chat):
            start_question_at(message.chat, 'question_3')
            bot.send_message(message.chat.id,
                             '_У каждой машины есть свои обычные характеристики._\n'
                             '\n'
                             '*Например:* _количество лошадиных сил, рабочий объём двигателя, длина корпуса и т.д. '
                             'Но это скучные данные...\n'
                             '\n'
                             'Другое дело, знать о машине её историю! Давайте представим, что у машин есть свой '
                             'исторический паспорт, в котором вместо характеристик указаны факты о ней_ 🥰',
                             parse_mode="Markdown", )
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIDv2SQgGfbwD80wGlZfVpuguEdiVIfAAJFzTEbaTaJSAUJHtj5F2RKAQADAgADeQADLwQ',
                           caption='Вам будут представлены исторические факты о машине. Предположите, о какой идёт '
                                   'речь. Есть несколько попыток!\n'
                                   '\n'
                                   '🚙 _В ответ название или «кличку» автомобиля_', parse_mode="Markdown")
            bot.register_next_step_handler(message, question_3_1)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_3: {error}')
        bot.register_next_step_handler(message, question_3)


def question_3_1(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["ваз-2101", "копейка", "ваз 2101", "ваз 2101", "ваз-2101", "ваз2101"]:
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDxWSQgxhyRWsKvRtMGIe_LyZHFauyAAJTzTEbaTaJSLJlVCJD3tSSAQADAgADeQADLwQ',
                               '_Отлично, молодцы!_ 👍🏼👍🏼👍🏼',
                               parse_mode="Markdown",
                               )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDwGSQgPB07vN5wuAOybIowcXdKYPCAAJHzTEbaTaJSO8MmfAFPfufAQADAgADeQADLwQ',
                               caption='_Водитель красного ВАЗ-2101 явно не хотел попасть в такую ситуацию, но '
                                       'фотография у него получилась достаточно колоритная._\n'
                                       '\n'
                                       '_Сможете показать как бы вы вели себя, если б вас остановили на '
                                       'такой машине?_ 🚗', parse_mode="Markdown",
                               )
                bot.register_next_step_handler(message, question_3_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDwWSQgXzcM2hSsyB-cajBLfvmntVgAAJJzTEbaTaJSNkdE-QFB4H8AQADAgADeQADLwQ',
                               caption='_Хм.. предлагаю подумать ещё_ 😊\n',
                               parse_mode="Markdown")
                bot.register_next_step_handler(message, question_3_2)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_3_1: {error}')
        bot.register_next_step_handler(message, question_3_1)


def question_3_2(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["ваз-2101", "копейка", "ваз 2101", "ваз 2101", "ваз-2101", "ваз2101"]:
                bot.send_message(message.chat.id,
                                 '_Отлично, молодцы!_ 👍🏼👍🏼👍🏼',
                                 parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDxWSQgxhyRWsKvRtMGIe_LyZHFauyAAJTzTEbaTaJSLJlVCJD3tSSAQADAgADeQADLwQ',
                               caption='_Водитель красного ВАЗ-2101 явно не хотел попасть в такую ситуацию, но '
                                       'фотография у него получилась достаточно колоритная._\n'
                                       '\n'
                                       '_Сможете показать как бы вы вели себя, если б вас остановили на '
                                       'такой машине?_ 🚗', parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDwGSQgPB07vN5wuAOybIowcXdKYPCAAJHzTEbaTaJSO8MmfAFPfufAQADAgADeQADLwQ')
                bot.register_next_step_handler(message, question_3_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDwmSQgpERGqJk1IwYuXW7fueJe6N-AAJPzTEbaTaJSGYsn-yiKXFJAQADAgADeQADLwQ',
                               caption='_Хм.. предлагаю подумать ещё_ 😊\n',
                               parse_mode="Markdown")
                bot.register_next_step_handler(message, question_3_3)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_3_2: {error}')
        bot.register_next_step_handler(message, question_3_2)


def question_3_3(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["ваз-2101", "копейка", "ваз 2101", "ваз 2101", "ваз-2101", "ваз2101"]:
                bot.send_message(message.chat.id,
                                 '_Отлично, молодцы!_ 👍🏼👍🏼👍🏼',
                                 parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDxWSQgxhyRWsKvRtMGIe_LyZHFauyAAJTzTEbaTaJSLJlVCJD3tSSAQADAgADeQADLwQ',
                               caption='_Водитель красного ВАЗ-2101 явно не хотел попасть в такую ситуацию, но '
                                       'фотография у него получилась достаточно колоритная._\n'
                                       '\n'
                                       '_Сможете показать как бы вы вели себя, если б вас остановили на '
                                       'такой машине?_ 🚗', parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDwGSQgPB07vN5wuAOybIowcXdKYPCAAJHzTEbaTaJSO8MmfAFPfufAQADAgADeQADLwQ')
                bot.register_next_step_handler(message, question_3_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDw2SQgr-C5-_xdE7ejvRcU0Dbn3s_AAJQzTEbaTaJSIQ6TNIuYCv0AQADAgADeQADLwQ',
                               caption='_Хм.. предлагаю подумать ещё_ 😊\n',
                               parse_mode="Markdown")
                bot.register_next_step_handler(message, question_3_4)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_3_3: {error}')
        bot.register_next_step_handler(message, question_3_3)


def question_3_4(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["ваз-2101", "копейка", "ваз 2101", "ваз 2101", "ваз-2101", "ваз2101"]:
                bot.send_message(message.chat.id,
                                 '_Отлично, молодцы!_ 👍🏼👍🏼👍🏼',
                                 parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDxWSQgxhyRWsKvRtMGIe_LyZHFauyAAJTzTEbaTaJSLJlVCJD3tSSAQADAgADeQADLwQ',
                               caption='_Водитель красного ВАЗ-2101 явно не хотел попасть в такую ситуацию, но '
                                       'фотография у него получилась достаточно колоритная._\n'
                                       '\n'
                                       '_Сможете показать как бы вы вели себя, если б вас остановили на '
                                       'такой машине?_ 🚗', parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDwGSQgPB07vN5wuAOybIowcXdKYPCAAJHzTEbaTaJSO8MmfAFPfufAQADAgADeQADLwQ')
                bot.register_next_step_handler(message, question_3_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDxGSQgvXWmPA5OCFc5tOc_ZUDRd77AAJSzTEbaTaJSOnMO1Z7v8IEAQADAgADeQADLwQ',
                               caption='Хм.. предлагаю подумать ещё 😊\n',
                               parse_mode="Markdown")
                bot.register_next_step_handler(message, question_3_4)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_3_4: {error}')
        bot.register_next_step_handler(message, question_3_4)


def question_3_end(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["ваз-2101", "копейка", "ваз 2101", "ваз 2101", "ваз-2101", "ваз2101"]:
                bot.send_message(message.chat.id,
                                 '_Отлично, молодцы!_ 👍🏼👍🏼👍🏼',
                                 parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDxWSQgxhyRWsKvRtMGIe_LyZHFauyAAJTzTEbaTaJSLJlVCJD3tSSAQADAgADeQADLwQ',
                               caption='_Водитель красного ВАЗ-2101 явно не хотел попасть в такую ситуацию, но '
                                       'фотография у него получилась достаточно колоритная._\n'
                                       '\n'
                                       '_Сможете показать как бы вы вели себя, если б вас остановили на '
                                       'такой машине?_ 🚗', parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDwGSQgPB07vN5wuAOybIowcXdKYPCAAJHzTEbaTaJSO8MmfAFPfufAQADAgADeQADLwQ')
                bot.register_next_step_handler(message, question_3_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_3_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_3_end: {error}')
        bot.register_next_step_handler(message, question_3_end)


def question_3_photo(message):
    try:
        if check_end_time(message.chat):
            if message.content_type == 'photo':
                keyboard_inline = types.InlineKeyboardMarkup()
                confirm_button = types.InlineKeyboardButton('Подтвердить', callback_data='confirm')
                cancel_button = types.InlineKeyboardButton('Отменить', callback_data='cancel')
                keyboard_inline.row(confirm_button, cancel_button)
                bot.send_photo(admin_id, message.photo[-1].file_id,
                               caption=f'Подтвердите отправку этой фотографии для "{message.chat.title}":\n'
                                       f'\n'
                                       f'Задание 3 (ваз2101):\n'
                                       f'\n'
                                       f'[ {message.chat} ]'
                                       f'#question_3#',
                               reply_markup=keyboard_inline)

                @bot.callback_query_handler(func=lambda call: True)
                def callback_handler(call):
                    text = call.message.caption
                    match = re.search(r'\[(.*?)\]', text)
                    question = re.search(r'\#(.*?)\#', text)
                    text = match.group(1).replace("'", "\"")
                    text_end = text.replace("None", "null")
                    value = json.loads(text_end)
                    chat = types.Chat.de_json(value)
                    if call.data == 'confirm':
                        end_question_at(chat, question.group(1))
                        bot.send_message(call.from_user.id, f'Фотография подтверждена у \"{chat.title}\"')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(chat.id, 'Хм, уверен это фото оценят по достоинству.\nОткрывай меню, '
                                                  'поехали дальше 👍🏼', reply_markup=keyboard.keyboard(chat))
                        if check_final(chat):
                            end_at(chat)
                            bot.send_sticker(chat.id,
                                             'CAACAgIAAxkBAAEJWLJkjZnnq-9Z6FIKDa7Sjzjv2udGTgACaS8AAmjYaUgPYCMFmg1OtC8E')
                            bot.send_message(chat.id, 'Вау! 🥳🥳🥳\n'
                                                      '\n'
                                                      'Я в восторге от того, как хорошо вы разбираетесь в автомобилях.'
                                                      'Не каждый смог бы пройти все задания и ответить на все вопросы. '
                                                      'Ещё и ваши фотографии, аплодирую стоя.\n'
                                                      '\n'
                                                      'Скоро ведущий объявит результаты игры, а вы пока можете '
                                                      'ещё насладиться выставкой\n'
                                                      '❤️', reply_markup=None)
                    elif call.data == 'cancel':
                        bot.send_message(chat.id, 'Хм.. даю ещё шанс 😊')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(call.from_user.id, f'Фотография отменена у \"{chat.title}\"')
                        bot.register_next_step_handler(message, question_3_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_3_photo)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_3_photo: {error}')
        bot.register_next_step_handler(message, question_3_photo)


# -------------Вопрос 4---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'вопрос 4', content_types=['text'])
def question_4(message):
    try:
        if check_end_time(message.chat):
            start_question_at(message.chat, 'question_4')
            bot.send_message(message.chat.id,
                             '_На дороге одним из самых важных аспектов является_ *внимательность!* _Невнимательный '
                             'водитель может и поворот пропустить, и перекати-поле сбить, и поломанную машину '
                             'купить._\n'
                             '\n'
                             '_Чтобы с вами такого не случалось, есть отличная возможность потренировать это '
                             'качество прямо сейчас_ ✊🏼'
                             , parse_mode="Markdown", )
            bot.send_video(message.chat.id,
                           'BAACAgIAAxkBAAIDxmSQhP-zJlwYJdgPbOiWzn7ZST-JAALWMgACaTaJSDDU0KcWLNWuLwQ')
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIDyGSQiM_4Sg4Z4cPChl4gG8sKPCyAAAJpzTEbaTaJSC-DOLoK-jWZAQADAgADeQADLwQ',
                           caption='Ваша задача — внимательно посмотреть видео и ответить на вопросы после него '
                                   'в любом порядке.\n'
                                   '\n'
                                   '🚙 _Ответ на каждый вопрос присылайте отдельным сообщением._', parse_mode="Markdown")
            bot.register_next_step_handler(message, question_4_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_4: {error}')
        bot.register_next_step_handler(message, question_4)


def question_4_end(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ['3', 'три']:
                if check_answer(message.chat, 'question_answer', "answer_1"):
                    bot.send_message(message.chat.id,
                                     'Верно, но подобный ответ уже засчитан',
                                     parse_mode="Markdown", )
                    bot.register_next_step_handler(message, question_4_end)
                else:
                    bot.send_message(message.chat.id,
                                     'Прекрасно справляешься!',
                                     parse_mode="Markdown", )
                    change_answer(message.chat, 'question_answer', "answer_1")
                    if check_answer_final(message.chat, 'question_answer'):
                        bot.send_message(message.chat.id,
                                         '_Молодцы_ 💪🏼 _Теперь фото!_', parse_mode="Markdown", )
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAIDx2SQiHX4ValhuzyMmUqnn437dNc3AAJmzTEbaTaJSM6bNYh4O6hNAQADAgADeQADLwQ',
                                       caption='_Ух ты, вот это дааа! Смотрите, какая счастливая семья❤️ '
                                               'Вы своего рода тоже семья, ведь задания выполняете вместе!\n'
                                               '\n'
                                               'А сможете сделать такое же фото? Только не трогайте автомобиль, '
                                               'он и так старенький уже совсем_ 😅', parse_mode="Markdown"
                                       )
                        bot.register_next_step_handler(message, question_4_photo)
                    else:
                        bot.register_next_step_handler(message, question_4_end)
            elif message.text.lower() in ['красная', 'красного', 'бордовая', 'бордового']:
                if check_answer(message.chat, 'question_answer', "answer_2"):
                    bot.send_message(message.chat.id,
                                     'Верно, но подобный ответ уже засчитан',
                                     parse_mode="Markdown", )
                    bot.register_next_step_handler(message, question_4_end)
                else:
                    bot.send_message(message.chat.id,
                                     'Прекрасно справляешься!',
                                     parse_mode="Markdown", )
                    change_answer(message.chat, 'question_answer', "answer_2")
                    if check_answer_final(message.chat, 'question_answer'):
                        bot.send_message(message.chat.id,
                                         '_Молодцы_ 💪🏼 _Теперь фото!_', parse_mode="Markdown", )
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAIDx2SQiHX4ValhuzyMmUqnn437dNc3AAJmzTEbaTaJSM6bNYh4O6hNAQADAgADeQADLwQ',
                                       caption='_Ух ты, вот это дааа! Смотрите, какая счастливая семья❤️ '
                                               'Вы своего рода тоже семья, ведь задания выполняете вместе!\n'
                                               '\n'
                                               'А сможете сделать такое же фото? Только не трогайте автомобиль, '
                                               'он и так старенький уже совсем_ 😅', parse_mode="Markdown"
                                       )
                        bot.register_next_step_handler(message, question_4_photo)
                    else:
                        bot.register_next_step_handler(message, question_4_end)
            elif message.text.lower() in ['6000', '6 тысяч', 'шесть тысяч',  "6", "шесть"]:
                if check_answer(message.chat, 'question_answer', "answer_3"):
                    bot.send_message(message.chat.id,
                                     'Верно, но подобный ответ уже засчитан',
                                     parse_mode="Markdown", )
                    bot.register_next_step_handler(message, question_4_end)
                else:
                    bot.send_message(message.chat.id,
                                     'Прекрасно справляешься!',
                                     parse_mode="Markdown", )
                    change_answer(message.chat, 'question_answer', "answer_3")
                    if check_answer_final(message.chat, 'question_answer'):
                        bot.send_message(message.chat.id,
                                         '_Молодцы_ 💪🏼 _Теперь фото!_', parse_mode="Markdown", )
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAIDx2SQiHX4ValhuzyMmUqnn437dNc3AAJmzTEbaTaJSM6bNYh4O6hNAQADAgADeQADLwQ',
                                       caption='_Ух ты, вот это дааа! Смотрите, какая счастливая семья❤️ '
                                               'Вы своего рода тоже семья, ведь задания выполняете вместе!\n'
                                               '\n'
                                               'А сможете сделать такое же фото? Только не трогайте автомобиль, '
                                               'он и так старенький уже совсем_ 😅', parse_mode="Markdown"
                                       )
                        bot.register_next_step_handler(message, question_4_photo)
                    else:
                        bot.register_next_step_handler(message, question_4_end)
            elif message.text.lower() in ['ford', 'ford model a', 'форд', 'форд модел а']:
                if check_answer(message.chat, 'question_answer', "answer_4"):
                    bot.send_message(message.chat.id,
                                     'Верно, но подобный ответ уже засчитан',
                                     parse_mode="Markdown", )
                    bot.register_next_step_handler(message, question_4_end)
                else:
                    bot.send_message(message.chat.id,
                                     'Прекрасно справляешься!',
                                     parse_mode="Markdown", )
                    change_answer(message.chat, 'question_answer', "answer_4")
                    if check_answer_final(message.chat, 'question_answer'):
                        bot.send_message(message.chat.id,
                                         '_Молодцы_ 💪🏼 _Теперь фото!_', parse_mode="Markdown", )
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAIDx2SQiHX4ValhuzyMmUqnn437dNc3AAJmzTEbaTaJSM6bNYh4O6hNAQADAgADeQADLwQ',
                                       caption='_Ух ты, вот это дааа! Смотрите, какая счастливая семья❤️ '
                                               'Вы своего рода тоже семья, ведь задания выполняете вместе!\n'
                                               '\n'
                                               'А сможете сделать такое же фото? Только не трогайте автомобиль, '
                                               'он и так старенький уже совсем_ 😅',parse_mode="Markdown")
                        bot.register_next_step_handler(message, question_4_photo)
                    else:
                        bot.register_next_step_handler(message, question_4_end)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_4_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_4_end: {error}')
        bot.register_next_step_handler(message, question_4_end)


def question_4_photo(message):
    try:
        if check_end_time(message.chat):
            if message.content_type == 'photo':
                keyboard_inline = types.InlineKeyboardMarkup()
                confirm_button = types.InlineKeyboardButton('Подтвердить', callback_data='confirm')
                cancel_button = types.InlineKeyboardButton('Отменить', callback_data='cancel')
                keyboard_inline.row(confirm_button, cancel_button)
                bot.send_photo(admin_id, message.photo[-1].file_id,
                               caption=f'Подтвердите отправку этой фотографии для "{message.chat.title}":\n'
                                       f'\n'
                                       f'Задание 4 (сбор ответов):\n'
                                       f'\n'
                                       f'[ {message.chat} ]'
                                       f'#question_4#',
                               reply_markup=keyboard_inline)

                @bot.callback_query_handler(func=lambda call: True)
                def callback_handler(call):
                    text = call.message.caption
                    match = re.search(r'\[(.*?)\]', text)
                    question = re.search(r'\#(.*?)\#', text)
                    text = match.group(1).replace("'", "\"")
                    text_end = text.replace("None", "null")
                    value = json.loads(text_end)
                    chat = types.Chat.de_json(value)
                    if call.data == 'confirm':
                        end_question_at(chat, question.group(1))
                        bot.send_message(call.from_user.id, f'Фотография подтверждена у \"{chat.title}\"')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(chat.id, 'Хм, уверен это фото оценят по достоинству.\nОткрывай меню, '
                                                  'поехали дальше 👍🏼', reply_markup=keyboard.keyboard(chat))
                        if check_final(chat):
                            end_at(chat)
                            bot.send_sticker(chat.id,
                                             'CAACAgIAAxkBAAEJWLJkjZnnq-9Z6FIKDa7Sjzjv2udGTgACaS8AAmjYaUgPYCMFmg1OtC8E')
                            bot.send_message(chat.id, 'Вау! 🥳🥳🥳\n'
                                                      '\n'
                                                      'Я в восторге от того, как хорошо вы разбираетесь в автомобилях.'
                                                      'Не каждый смог бы пройти все задания и ответить на все вопросы. '
                                                      'Ещё и ваши фотографии, аплодирую стоя.\n'
                                                      '\n'
                                                      'Скоро ведущий объявит результаты игры, а вы пока можете '
                                                      'ещё насладиться выставкой\n'
                                                      '❤️', reply_markup=None)
                    elif call.data == 'cancel':
                        bot.send_message(chat.id, 'Хм.. даю ещё шанс 😊')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(call.from_user.id, f'Фотография отменена у \"{chat.title}\"')
                        bot.register_next_step_handler(message, question_4_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_4_photo)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_4_photo: {error}')
        bot.register_next_step_handler(message, question_4_photo)


# -------------Вопрос 5---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'вопрос 5', content_types=['text'])
def question_5(message):
    try:
        if check_end_time(message.chat):
            start_question_at(message.chat, 'question_5')
            bot.send_message(message.chat.id,
                             '_Ух ты, вот это дааа! Смотрите, какая счастливая семья_❤️ _Вы своего рода тоже семья, '
                             'ведь задания выполняете вместе!_\n'
                             '\n'
                             '_Возьмите из бардачка записку, на ней бывший владелец оставил вам подсказку, '
                             'что же это за машина._', parse_mode="Markdown", )
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIDyWSQv95ZYo66Mic38g0txl0Of-OIAAKGzjEbaTaJSG9pCihb0tX5AQADAgADeQADLwQ')
            bot.register_next_step_handler(message, question_5_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_5: {error}')
        bot.register_next_step_handler(message, question_5)


def question_5_end(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["газ13", "газ-13", "газ 13", "чайка", "волга"]:

                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDymSQwBJDGXvY7p9TN0sPpOrbdeeoAAKIzjEbaTaJSFs4a-DLnZuzAQADAgADeQADLwQ',
                               caption='_Молодцы. Софи Лорен сфоткалась и вы сможете. Только вам надо повторить, '
                                       'успехов!_', parse_mode="Markdown", )
                bot.register_next_step_handler(message, question_5_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_5_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_5_end: {error}')
        bot.register_next_step_handler(message, question_5_end)


def question_5_photo(message):
    try:
        if check_end_time(message.chat):
            if message.content_type == 'photo':
                keyboard_inline = types.InlineKeyboardMarkup()
                confirm_button = types.InlineKeyboardButton('Подтвердить', callback_data='confirm')
                cancel_button = types.InlineKeyboardButton('Отменить', callback_data='cancel')
                keyboard_inline.row(confirm_button, cancel_button)
                bot.send_photo(admin_id, message.photo[-1].file_id,
                               caption=f'Подтвердите отправку этой фотографии для "{message.chat.title}":\n'
                                       f'\n'
                                       f'Задание 5 (газ13):\n'
                                       f'\n'
                                       f'[ {message.chat} ]'
                                       f'#question_5#',
                               reply_markup=keyboard_inline)

                @bot.callback_query_handler(func=lambda call: True)
                def callback_handler(call):
                    text = call.message.caption
                    match = re.search(r'\[(.*?)\]', text)
                    question = re.search(r'\#(.*?)\#', text)
                    text = match.group(1).replace("'", "\"")
                    text_end = text.replace("None", "null")
                    value = json.loads(text_end)
                    chat = types.Chat.de_json(value)
                    if call.data == 'confirm':
                        end_question_at(chat, question.group(1))
                        bot.send_message(call.from_user.id, f'Фотография подтверждена у \"{chat.title}\"')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(chat.id, 'Хм, уверен это фото оценят по достоинству.\nОткрывай меню, '
                                                  'поехали дальше 👍🏼', reply_markup=keyboard.keyboard(chat))
                        if check_final(chat):
                            end_at(chat)
                            bot.send_sticker(chat.id,
                                             'CAACAgIAAxkBAAEJWLJkjZnnq-9Z6FIKDa7Sjzjv2udGTgACaS8AAmjYaUgPYCMFmg1OtC8E')
                            bot.send_message(chat.id, 'Вау! 🥳🥳🥳\n'
                                                      '\n'
                                                      'Я в восторге от того, как хорошо вы разбираетесь в автомобилях.'
                                                      'Не каждый смог бы пройти все задания и ответить на все вопросы. '
                                                      'Ещё и ваши фотографии, аплодирую стоя.\n'
                                                      '\n'
                                                      'Скоро ведущий объявит результаты игры, а вы пока можете '
                                                      'ещё насладиться выставкой\n'
                                                      '❤️', reply_markup=None)
                    elif call.data == 'cancel':
                        bot.send_message(chat.id, 'Хм.. даю ещё шанс 😊')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(call.from_user.id, f'Фотография отменена у \"{chat.title}\"')
                        bot.register_next_step_handler(message, question_5_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_5_photo)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_5_photo: {error}')
        bot.register_next_step_handler(message, question_5_photo)


# -------------Вопрос 6---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'вопрос 6', content_types=['text'])
def question_6(message):
    try:
        if check_end_time(message.chat):
            start_question_at(message.chat, 'question_6')
            bot.send_message(message.chat.id,
                             '_Кто-то милого способен узнать по походке, ну мы с вами легко отгадаем машину даже с '
                             'закрытыми глазами! Ну ладно… с силуэтом машины  будет, пожалуй, проще._'
                             , parse_mode="Markdown", )
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIDy2SQwUHg1w_qRzHRgRHNj1-CdP1nAAKNzjEbaTaJSGawCC0rmviPAQADAgADeAADLwQ',
                           caption='🚙 _Напишите марку машины, которую мы скрыли_', parse_mode="Markdown")
            bot.register_next_step_handler(message, question_6_1)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_6: {error}')
        bot.register_next_step_handler(message, question_6)


def question_6_1(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["астон мартин", "астонмартин", "aston martin", "astonmartin"]:
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDz2SQw3EieP4bX6tYzSAbYuaBppPwAAIUyDEbGVaISDuWpytb4seHAQADAgADeQADLwQ')
                bot.send_message(message.chat.id,
                                 '_Супер, держите еще машину. _'
                                 , parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDzWSQwjVRhYROr5yFyTcdN1D7hxyuAAKQzjEbaTaJSEvie_tfbnCaAQADAgADeQADLwQ')
                bot.register_next_step_handler(message, question_6_2)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_6_1)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_6_1: {error}')
        bot.register_next_step_handler(message, question_6_1)


def question_6_2(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["альфа ромео", "альфаромео", "alfa romeo", "alfaromeo"]:
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAID0GSQw7aRqDzlQcHSSQ0zWVW2Bk7MAAIVyDEbGVaISLT166vZBHvKAQADAgADbQADLwQ')
                bot.send_message(message.chat.id,
                                 '_Супер, держите еще машину._'
                                 , parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIDzmSQwpyPpjcPgNBo9YbM_kLEERsFAAITyDEbGVaISFG-dv9yUayPAQADAgADeQADLwQ')
                bot.register_next_step_handler(message, question_6_end)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_6_2)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_6_2: {error}')
        bot.register_next_step_handler(message, question_6_2)


def question_6_end(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ["aurus", "аурус", "аурус сенат", "aurus senat"]:
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAID0WSQxAQ597I8kZRtNdjyp5y6RksUAAIWyDEbGVaISPotVq15ct0TAQADAgADeQADLwQ',
                               )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAID0mSQxEMQMRoyTdhlgZikmZHjLIDqAAIXyDEbGVaISCfYIT-rtZFSAQADAgADeQADLwQ',
                               caption='_Молодцы. '
                                       'Ну_…_не знаю как вы будете повторять следующее фото 😂 Вот и проверим, '
                                       'на что способна ваша фантазия!_'
                               , parse_mode="Markdown"
                               )
                bot.register_next_step_handler(message, question_6_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_6_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_6_end: {error}')
        bot.register_next_step_handler(message, question_6_end)


def question_6_photo(message):
    try:
        if check_end_time(message.chat):
            if message.content_type == 'photo':
                keyboard_inline = types.InlineKeyboardMarkup()
                confirm_button = types.InlineKeyboardButton('Подтвердить', callback_data='confirm')
                cancel_button = types.InlineKeyboardButton('Отменить', callback_data='cancel')
                keyboard_inline.row(confirm_button, cancel_button)
                bot.send_photo(admin_id, message.photo[-1].file_id,
                               caption=f'Подтвердите отправку этой фотографии для "{message.chat.title}":\n'
                                       f'\n'
                                       f'Задание 6 (Силуэты):\n'
                                       f'\n'
                                       f'[ {message.chat} ]'
                                       f'#question_6#',
                               reply_markup=keyboard_inline)

                @bot.callback_query_handler(func=lambda call: True)
                def callback_handler(call):
                    text = call.message.caption
                    match = re.search(r'\[(.*?)\]', text)
                    question = re.search(r'\#(.*?)\#', text)
                    text = match.group(1).replace("'", "\"")
                    text_end = text.replace("None", "null")
                    value = json.loads(text_end)
                    chat = types.Chat.de_json(value)
                    if call.data == 'confirm':
                        end_question_at(chat, question.group(1))
                        bot.send_message(call.from_user.id, f'Фотография подтверждена у \"{chat.title}\"')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(chat.id, 'Хм, уверен это фото оценят по достоинству.\nОткрывай меню, '
                                                  'поехали дальше 👍🏼', reply_markup=keyboard.keyboard(chat))
                        if check_final(chat):
                            end_at(chat)
                            bot.send_sticker(chat.id,
                                             'CAACAgIAAxkBAAEJWLJkjZnnq-9Z6FIKDa7Sjzjv2udGTgACaS8AAmjYaUgPYCMFmg1OtC8E')
                            bot.send_message(chat.id, 'Вау! 🥳🥳🥳\n'
                                                      '\n'
                                                      'Я в восторге от того, как хорошо вы разбираетесь в автомобилях.'
                                                      'Не каждый смог бы пройти все задания и ответить на все вопросы. '
                                                      'Ещё и ваши фотографии, аплодирую стоя.\n'
                                                      '\n'
                                                      'Скоро ведущий объявит результаты игры, а вы пока можете '
                                                      'ещё насладиться выставкой\n'
                                                      '❤️', reply_markup=None)
                    elif call.data == 'cancel':
                        bot.send_message(chat.id, 'Хм.. даю ещё шанс 😊')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(call.from_user.id, f'Фотография отменена у \"{chat.title}\"')
                        bot.register_next_step_handler(message, question_6_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_6_photo)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_6_photo: {error}')
        bot.register_next_step_handler(message, question_6_photo)


# -------------Вопрос 7*---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'вопрос 7', content_types=['text'])
def question_7(message):
    try:
        if check_end_time(message.chat):
            start_question_at(message.chat, 'question_7')
            bot.send_message(message.chat.id,
                             '_Часто в сервисных центрах водители не могут нормально объяснить, что у них '
                             'за поломка._\n'
                             '\n'
                             '🚙 _По описаниям таких водителей необходимо понять, что у них сломалось и прислать '
                             'стикер детали, которую нужно починить._'
                             , parse_mode="Markdown", )
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEJWLRkjZpdhGap32r3QBh7xTfAKbc_twAC9TAAAhP4aUjeuMcerREJFi8E')
            bot.send_message(message.chat.id,
                             '_Сохраните стикерпак_'
                             , parse_mode="Markdown", )
            bot.send_voice(message.chat.id, 'AwACAgQAAxkBAAIHwGSTSizZF-5u9SPVT6VIXc8Rg5DuAAJXSQACc9WZUG_M1CeDDtNdLwQ')
            bot.register_next_step_handler(message, question_7_1)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_7: {error}')
        bot.register_next_step_handler(message, question_5)


def question_7_1(message):
    try:
        if check_end_time(message.chat):
            if message.sticker.emoji == "2️⃣" and message.sticker.set_name == 'Vysshaya_peredacha':
                bot.send_message(message.chat.id,
                                 '_Конечно это скрипят колодки. Посмотрим какие поломки у остальных. _'
                                 , parse_mode="Markdown", )
                bot.send_voice(message.chat.id,
                               'AwACAgQAAxkBAAIHwWSTTVaY460iNn-npAYC_rG4iZz6AAKCSgACc9WZUAABt0avhcJiQy8E')

                bot.register_next_step_handler(message, question_7_2)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_7_1)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_7_1: {error}')
        bot.register_next_step_handler(message, question_7_1)


def question_7_2(message):
    try:
        if check_end_time(message.chat):
            if message.sticker.emoji == "1️⃣" and message.sticker.set_name == 'Vysshaya_peredacha':
                bot.send_message(message.chat.id,
                                 '_Да, здесь явно проблема со стартером. Что там еще  сломалось у последнего клиента?_'
                                 , parse_mode="Markdown", )
                bot.send_voice(message.chat.id,
                               'AwACAgQAAxkBAAIHwmSTTu3EsrAlXNWRCrplseP8HqvnAAIESwACc9WZUMa-tgABcpUYDC8E')
                bot.register_next_step_handler(message, question_7_3)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_7_2)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_7_2: {error}')
        bot.register_next_step_handler(message, question_7_2)


def question_7_3(message):
    try:
        if check_end_time(message.chat):
            if message.sticker.emoji == "3️⃣" and message.sticker.set_name == 'Vysshaya_peredacha':
                bot.send_message(message.chat.id,
                                 "_Да, тут, скорее всего, проблемы с прокладкой головки цилиндра.\n"
                                 "Молодцы, вы помогли всем_🤝", parse_mode="Markdown", )
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIGwGSTKWTdTORi8lwAARIv3cwDWBYybQACY8oxG7TXmEiNs9zD0vJ5hgEAAwIAA3kAAy8E')
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIGwWSTKXdVxrW3cbCZVVtdCISbSQKIAAJkyjEbtNeYSE_zi2tOUAZXAQADAgADeQADLwQ',
                               caption="_Кстати, как вы думаете, могли ли такие проблемы возникнуть у владельца "
                                       "уникального в своем роде автомобиля? Ведь ZIBAR-MK 2 это уникальный вездеход, "
                                       "который выдерживает даже жару в +55 и может адаптироваться практически под "
                                       "любые требования.Чем-то даже напоминает машину Бэтмена. Вот вам фото этого "
                                       "вездехода и Бэтмена с его бэмобилем. Сделайте с ним такое же фото, как "
                                       "известный супергерой. Кстати, чем больше вас будет на фото, тем лучше._"
                               , parse_mode="Markdown")
                bot.register_next_step_handler(message, question_7_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_7_3)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_7_3: {error}')
        bot.register_next_step_handler(message, question_7_3)


def question_7_photo(message):
    try:
        if check_end_time(message.chat):
            if message.content_type == 'photo':
                keyboard_inline = types.InlineKeyboardMarkup()
                confirm_button = types.InlineKeyboardButton('Подтвердить', callback_data='confirm')
                cancel_button = types.InlineKeyboardButton('Отменить', callback_data='cancel')
                keyboard_inline.row(confirm_button, cancel_button)
                bot.send_photo(admin_id, message.photo[-1].file_id,
                               caption=f'Подтвердите отправку этой фотографии для "{message.chat.title}":\n'
                                       f'\n'
                                       f'Задание 7 (Поломки):\n'
                                       f'\n'
                                       f'[ {message.chat} ]'
                                       f'#question_7#',
                               reply_markup=keyboard_inline)

                @bot.callback_query_handler(func=lambda call: True)
                def callback_handler(call):
                    text = call.message.caption
                    match = re.search(r'\[(.*?)\]', text)
                    question = re.search(r'\#(.*?)\#', text)
                    text = match.group(1).replace("'", "\"")
                    text_end = text.replace("None", "null")
                    value = json.loads(text_end)
                    chat = types.Chat.de_json(value)
                    if call.data == 'confirm':
                        end_question_at(chat, question.group(1))
                        bot.send_message(call.from_user.id, f'Фотография подтверждена у \"{chat.title}\"')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(chat.id, 'Хм, уверен это фото оценят по достоинству.\nОткрывай меню, '
                                                  'поехали дальше 👍🏼', reply_markup=keyboard.keyboard(chat))
                        if check_final(chat):
                            end_at(chat)
                            bot.send_sticker(chat.id,
                                             'CAACAgIAAxkBAAEJWLJkjZnnq-9Z6FIKDa7Sjzjv2udGTgACaS8AAmjYaUgPYCMFmg1OtC8E')
                            bot.send_message(chat.id, '_Вау! Я в восторге от того, как хорошо вы разбираетесь в '
                                                      'автомобилях.Не каждый смог бы пройти все задания и '
                                                      'ответить на все вопросы. Еще и ваши фотографии, аплодирую '
                                                      'стоя. Скоро ведущий объявит результаты игры, а вы пока '
                                                      'можете еще насладиться выставкой._', reply_markup=None)
                    elif call.data == 'cancel':
                        bot.send_message(chat.id, 'Хм.. даю ещё шанс 😊')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(call.from_user.id, f'Фотография отменена у \"{chat.title}\"')
                        bot.register_next_step_handler(message, question_7_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_7_photo)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_7_photo: {error}')
        bot.register_next_step_handler(message, question_7_photo)


# -------------Вопрос 8*---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'вопрос 8', content_types=['text'])
def question_8(message):
    try:
        if check_end_time(message.chat):
            start_question_at(message.chat, 'question_8')
            bot.send_message(message.chat.id,
                             '_Николай, Арсений, Иван и Ян собрались покупать себе машины через сервис Авито. '
                             'У каждого из них есть пожелания по марке автомобиля, цвету и цене, в соответствии '
                             'с их возрастом. Давайте узнаем, кто же, что себе хочет купить. _'
                             , parse_mode="Markdown", )
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAID3WSQyynG8xF1VeKkscm2cnl95Y-qAAK0zjEbaTaJSESysD0NqZZSAQADAgADeQADLwQ')
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAID3mSQyzxNLh3TzGJgKvmyAnSQ7cDAAAK1zjEbaTaJSFnQNIemhmjaAQADAgADeQADLwQ')
            bot.send_message(message.chat.id,
                             'Сопоставьте все факты и определите будущих владельцев авто!\n'
                             '\n'
                             '🚙 _Один ответ = один автовладелец. Пример: Николай-машина_'
                             , parse_mode="Markdown", )
            bot.register_next_step_handler(message, question_8_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_8: {error}')
        bot.register_next_step_handler(message, question_8)


def question_8_end(message):
    try:
        if check_end_time(message.chat):
            if message.text.lower() in ['николай-девятка']:
                if check_answer(message.chat, 'question_answer_end', "answer_1"):
                    bot.send_message(message.chat.id,
                                     'Верно, но подобный ответ уже засчитан',
                                     parse_mode="Markdown", )
                    bot.register_next_step_handler(message, question_8_end)
                else:
                    bot.send_message(message.chat.id,
                                     'Прекрасно справляешься!',
                                     parse_mode="Markdown", )
                    change_answer(message.chat, 'question_answer_end', "answer_1")
                    if check_answer_final(message.chat, 'question_answer_end'):
                        bot.send_message(message.chat.id,
                                         '_Молодцы. Так, это салон Майбаха, если что. Напоминаю, наша задача – повторить фото. Трогать машину нельзя, но вы попробуйте подобрать хотя бы ракурс похожий) У вас всё получится!_',
                                         parse_mode="Markdown", )
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAID32SQzbW7N8Hy25H21op_h3nuKSyTAAK5zjEbaTaJSMChYhqcuio8AQADAgADeQADLwQ')
                        bot.register_next_step_handler(message, question_8_photo)
                    else:
                        bot.register_next_step_handler(message, question_8_end)
            elif message.text.lower() in ['арсений-бмв', 'арсений-bmw']:
                if check_answer(message.chat, 'question_answer_end', "answer_2"):
                    bot.send_message(message.chat.id,
                                     'Верно, но подобный ответ уже засчитан',
                                     parse_mode="Markdown", )
                    bot.register_next_step_handler(message, question_8_end)
                else:
                    bot.send_message(message.chat.id,
                                     'Прекрасно справляешься!',
                                     parse_mode="Markdown", )
                    change_answer(message.chat, 'question_answer_end', "answer_2")
                    if check_answer_final(message.chat, 'question_answer_end'):
                        bot.send_message(message.chat.id,
                                         '_Молодцы. Так, это салон Майбаха, если что. Напоминаю, наша задача – '
                                         'повторить фото. Трогать машину нельзя, но вы попробуйте подобрать хотя '
                                         'бы ракурс похожий) У вас всё получится!_', parse_mode="Markdown", )
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAID32SQzbW7N8Hy25H21op_h3nuKSyTAAK5zjEbaTaJSMChYhqcuio8AQADAgADeQADLwQ')
                        bot.register_next_step_handler(message, question_8_photo)
                    else:
                        bot.register_next_step_handler(message, question_8_end)
            elif message.text.lower() in ['иван-майбах', 'иван-maybach']:
                if check_answer(message.chat, 'question_answer_end', "answer_3"):
                    bot.send_message(message.chat.id,
                                     'Верно, но подобный ответ уже засчитан',
                                     parse_mode="Markdown", )
                    bot.register_next_step_handler(message, question_8_end)
                else:
                    bot.send_message(message.chat.id,
                                     'Прекрасно справляешься!',
                                     parse_mode="Markdown", )
                    change_answer(message.chat, 'question_answer_end', "answer_3")
                    if check_answer_final(message.chat, 'question_answer_end'):
                        bot.send_message(message.chat.id,
                                         '_Молодцы. Так, это салон Майбаха, если что. Напоминаю, наша задача – '
                                         'повторить фото. Трогать машину нельзя, но вы попробуйте подобрать хотя '
                                         'бы ракурс похожий) У вас всё получится!_', parse_mode="Markdown", )
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAID32SQzbW7N8Hy25H21op_h3nuKSyTAAK5zjEbaTaJSMChYhqcuio8AQADAgADeQADLwQ')
                        bot.register_next_step_handler(message, question_8_photo)
                    else:
                        bot.register_next_step_handler(message, question_8_end)
            elif message.text.lower() in ['ян-ауди', 'ян-audi']:
                if check_answer(message.chat, 'question_answer_end', "answer_4"):
                    bot.send_message(message.chat.id,
                                     'Верно, но подобный ответ уже засчитан',
                                     parse_mode="Markdown", )
                    bot.register_next_step_handler(message, question_8_end)
                else:
                    bot.send_message(message.chat.id,
                                     'Прекрасно справляешься!',
                                     parse_mode="Markdown", )
                    change_answer(message.chat, 'question_answer_end', "answer_4")
                    if check_answer_final(message.chat, 'question_answer_end'):
                        bot.send_message(message.chat.id,
                                         '_Молодцы. Так, это салон Майбаха, если что. Напоминаю, наша задача – '
                                         'повторить фото. Трогать машину нельзя, но вы попробуйте подобрать хотя '
                                         'бы ракурс похожий) У вас всё получится!_', parse_mode="Markdown", )
                        bot.send_photo(message.chat.id,
                                       'AgACAgIAAxkBAAID32SQzbW7N8Hy25H21op_h3nuKSyTAAK5zjEbaTaJSMChYhqcuio8AQADAgADeQADLwQ')
                        bot.register_next_step_handler(message, question_8_photo)
                    else:
                        bot.register_next_step_handler(message, question_8_end)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_8_end)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_8_end: {error}')
        bot.register_next_step_handler(message, question_8_end)


def question_8_photo(message):
    try:
        if check_end_time(message.chat):
            if message.content_type == 'photo':
                keyboard_inline = types.InlineKeyboardMarkup()
                confirm_button = types.InlineKeyboardButton('Подтвердить', callback_data='confirm')
                cancel_button = types.InlineKeyboardButton('Отменить', callback_data='cancel')
                keyboard_inline.row(confirm_button, cancel_button)
                bot.send_photo(admin_id, message.photo[-1].file_id,
                               caption=f'Подтвердите отправку этой фотографии для "{message.chat.title}":\n'
                                       f'\n'
                                       f'Задание 8 (Эйнштейн ):\n'
                                       f'\n'
                                       f'[ {message.chat} ]'
                                       f'#question_8#',
                               reply_markup=keyboard_inline)

                @bot.callback_query_handler(func=lambda call: True)
                def callback_handler(call):
                    text = call.message.caption
                    match = re.search(r'\[(.*?)\]', text)
                    question = re.search(r'\#(.*?)\#', text)
                    text = match.group(1).replace("'", "\"")
                    text_end = text.replace("None", "null")
                    value = json.loads(text_end)
                    chat = types.Chat.de_json(value)
                    if call.data == 'confirm':
                        end_question_at(chat, question.group(1))
                        bot.send_message(call.from_user.id, f'Фотография подтверждена у \"{chat.title}\"')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(chat.id, 'Хм, уверен это фото оценят по достоинству.\nОткрывай меню, '
                                                  'поехали дальше 👍🏼', reply_markup=keyboard.keyboard(chat))
                        if check_final(chat):
                            end_at(chat)
                            bot.send_sticker(chat.id,
                                             'CAACAgIAAxkBAAEJWLJkjZnnq-9Z6FIKDa7Sjzjv2udGTgACaS8AAmjYaUgPYCMFmg1OtC8E')
                            bot.send_message(chat.id, 'Вау! 🥳🥳🥳\n'
                                                      '\n'
                                                      'Я в восторге от того, как хорошо вы разбираетесь в автомобилях.'
                                                      'Не каждый смог бы пройти все задания и ответить на все вопросы. '
                                                      'Ещё и ваши фотографии, аплодирую стоя.\n'
                                                      '\n'
                                                      'Скоро ведущий объявит результаты игры, а вы пока можете '
                                                      'ещё насладиться выставкой\n'
                                                      '❤️', reply_markup=None)
                    elif call.data == 'cancel':
                        bot.send_message(chat.id, 'Хм.. даю ещё шанс 😊')
                        bot.delete_message(call.from_user.id, call.message.id)
                        bot.send_message(call.from_user.id, f'Фотография отменена у \"{chat.title}\"')
                        bot.register_next_step_handler(message, question_8_photo)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                                 parse_mode="Markdown")
                bot.register_next_step_handler(message, question_8_photo)
        else:
            bot.send_message(message.chat.id,
                             '_Увы, время вышло_'
                             , parse_mode="Markdown")
    except Exception as error:
        print(f'question_8_photo: {error}')
        bot.register_next_step_handler(message, question_8_photo)


# -------------Вопрос конец---------------------------

def start_question_at(chat_data, name_colum):
    database = db.Data(chat_data)
    database.start_question_at(f'start_{name_colum}')


def end_question_at(chat_data, name_colum):
    database = db.Data(chat_data)
    database.end_question_at(f'{name_colum}')


def end_at(chat_data):
    database = db.Data(chat_data)
    database.end_at()

def check_final(chat_data):
    database = db.Data(chat_data)
    number = database.check_final()
    if all(number):
        return True
    else:
        return False


def check_end_time(chat_data):
    database = db.Data(chat_data)
    time_start_tuple = database.check_end_time()

    # Извлекаем объект времени из кортежа
    time_start = time_start_tuple[0]
    time_start_str = time_start.strftime('%H:%M:%S')

    now = datetime.now().time()
    start_time = datetime.strptime(time_start_str, '%H:%M:%S').time()
    end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=60)).time()

    if start_time <= now <= end_time:
        return True
    else:
        return False


# -------------------------------------------------
def change_answer(user_data, table_name, name_colum):
    database = db.Data(user_data)
    database.replace_answer(table_name, name_colum)


def check(user_id, name_colum):
    database = db.Data(user_id)
    number = database.check(name_colum)
    return number


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


while True:
    try:
        bot.polling(none_stop=True, timeout=5)
    except Exception as error:
        print(error)
        time.sleep(3)
