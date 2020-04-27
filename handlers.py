import logging
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import ConversationHandler

def greet_user(update, context):
    text = 'Вызван старт'
    logging.info(text)
    bot_text = 'Привет, я бот помощник.'
    update.message.reply_text(bot_text, reply_markup=get_keyboard())

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([
                                       ['Добраться до площадки', 'Связаться с организаторами', 'Поделиться ботом'],
                                       ['Список докладов', 'Проголосовать за доклады','Результаты голосования'],
                                       ['Оценить организацию', 'Календарь событий', 'Об Ozon Tech']
                                       ], resize_keyboard=True
                                    )
    return my_keyboard

def location(update, context):
    navigation_text = 'Выбери откуда тебе удобно добраться.'
    update.message.reply_text(navigation_text, reply_markup=get_keyboard_1())

def get_keyboard_1():
    my_keyboard_1 = ReplyKeyboardMarkup([
                                        ['От метро Выставочная', 'От метро Международная'],
                                        ['От МЦК Деловой центр', 'Я на машине'],
                                        ['Главное меню']
                                        ], resize_keyboard=True
                                    )
    return my_keyboard_1

def calendar(update, context):
    btn_site = [[InlineKeyboardButton('Мероприятия Ozon Tech', url='https://ozon.dev/events')]]
    reply_markup = InlineKeyboardMarkup(btn_site)
    update.message.reply_text('Тут можно узнать о ближайших событиях.', reply_markup = reply_markup)

def about(update, context):
    tech_about = [[InlineKeyboardButton('Об Ozon Tech', url='https://ozon.dev')]]
    reply_markup = InlineKeyboardMarkup(tech_about)
    update.message.reply_text('Тут можно узнать о технологиях.', reply_markup = reply_markup)

def contact(update, context):
    org_contact = 'James Marshall Hendrix +7(968) 381-56-10'
    update.message.reply_text(org_contact, reply_markup=get_keyboard())

def location_vist(update, context):
    update.message.reply_text('''Добраться от Выставочной''')
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/rick.jpg', 'rb'), reply_markup=get_keyboard())

def location_mejd(update, context):
    update.message.reply_text('''Добраться от Международной''')
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/rick.jpg', 'rb'), reply_markup=get_keyboard())

def location_mtsk(update, context):
    update.message.reply_text('''Добраться от МЦК''')
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/rick.jpg', 'rb'), reply_markup=get_keyboard())

def location_car(update, context):
    update.message.reply_text('''Добраться на машине''')
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/rick.jpg', 'rb'), reply_markup=get_keyboard())


def send_photo(update, context):
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/rick.jpg', 'rb'), reply_markup=get_keyboard())

#def talk_to_me(bot, update):
#    user_text = (update.message.chat.first_name, update.message.text)
#    logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username,
#                 update.message.chat.id, update.message.text)
#    update.message.reply_text(user_text, reply_markup=get_keyboard())

def org_assessment_start(update, context):
    update.message.reply_text("Как вас зовут?", reply_markup = ReplyKeyboardRemove())
    return 'name'

def org_assessment_get_name(update, context):
    context.user_data['user_name'] = update.message.text
    job_keyboard = [["0-1", "1-2"],
                    ["2-5", "5-10"]]

    update.message.reply_text(
        "Ваш опыт работы (в годах).",
        reply_markup=ReplyKeyboardMarkup(job_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return 'job'

def org_assessment_job(update, context):
    context.user_data['job'] = update.message.text
    poz_keyboard = [["Студент", "Junior"],
                    ["Middle", "Senior", "TeamLead"],
                    ["Manager", "Другое"]]

    update.message.reply_text(
        "Позиция",
        reply_markup=ReplyKeyboardMarkup(poz_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return 'poz'

def org_assessment_poz(update, context):
    context.user_data['poz'] = update.message.text
    assessment_keyboard = [["1", "2", "3", "4", "5"],
                           ["6", "7", "8", "9", "10"]]

    update.message.reply_text(
        "Оцените организацию мероприятия по шкале от 1 до 10",
        reply_markup=ReplyKeyboardMarkup(assessment_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return 'rating'

def org_assessment_rating(update, context):
    context.user_data['org_rating'] = update.message.text
    update.message.reply_text(""" Пожалуйста напишите пожелание/отзыв/критику в свободной
форме или вызовите /skip чтоб пропустить этот шаг. Нам важно ваше мнение. Спасибо!""")
    return 'comment'

def org_assessment_comment(update, context):
    context.user_data['org_comment'] = update.message.text
    text = """
<b>Имя:</b> {user_name}
<b>Опыт работы:</b> {job}
<b>Позиция:</b> {poz}
<b>Оценка:</b> {org_rating}
<b>Комментарий:</b> {org_comment}""".format(**context.user_data)
    update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    comm = 'Заполнен отзыв о мероприятии'
    logging.info(comm)
    return ConversationHandler.END

def org_assessment_comment_skip(update, context):
    text = """
<b>Имя:</b> {user_name}
<b>Опыт работы:</b> {job}
<b>Позиция:</b> {poz}
<b>Оценка:</b> {org_rating}""".format(**context.user_data)
    update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def dontknow(update, context):
    update.message.reply_text("Не понимаю")
