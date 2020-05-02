import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode
from telegram.ext import ConversationHandler

from db import db, get_or_create_user
from assessment import *
from handlers import *

def org_assessment_start(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    update.message.reply_text("Как вас зовут?", reply_markup = ReplyKeyboardRemove())
    return 'name'

def org_assessment_get_name(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    context.user_data['user_name'] = update.message.text
    job_keyboard = [["0-1", "1-2"],
                    ["2-5", "5-10"]]

    update.message.reply_text(
        "Ваш опыт работы (в годах).",
        reply_markup=ReplyKeyboardMarkup(job_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return 'job'

def org_assessment_job(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
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
    user = get_or_create_user(db, update.effective_user, update.message)
    context.user_data['poz'] = update.message.text
    assessment_keyboard = [["1", "2", "3", "4", "5"],
                           ["6", "7", "8", "9", "10"]]

    update.message.reply_text(
        "Оцените организацию мероприятия по шкале от 1 до 10",
        reply_markup=ReplyKeyboardMarkup(assessment_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return 'rating'

def org_assessment_rating(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    context.user_data['org_rating'] = update.message.text
    update.message.reply_text(""" Пожалуйста напишите пожелание/отзыв/критику в свободной
форме или вызовите /skip чтоб пропустить этот шаг. Нам важно ваше мнение. Спасибо!""")
    return 'comment'

def org_assessment_comment(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
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
    user = get_or_create_user(db, update.effective_user, update.message)
    text = """
<b>Имя:</b> {user_name}
<b>Опыт работы:</b> {job}
<b>Позиция:</b> {poz}
<b>Оценка:</b> {org_rating}""".format(**context.user_data)
    update.message.reply_text(text, reply_markup=get_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def dontknow(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    update.message.reply_text('Не понимаю')

