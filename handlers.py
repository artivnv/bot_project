import logging
import os

from emoji import emojize
from telegram import ReplyKeyboardMarkup, \
    InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, error
from telegram.ext import messagequeue as mq

from db import db, get_or_create_user, toggle_subscription, get_subscribers,\
    save_vote_for_reports

from location import *

def greet_user(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    text = 'Вызван старт'
    logging.info(text)
    bot_text = '''Привет, я бот помощник. Вот команды которые я понимаю.
/subscribe - подписаться на напоминание о мероприятии за два часа
/unsubscribe - отписаться от напоминания'''
    update.message.reply_text(bot_text, reply_markup=get_keyboard())

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([
                                       ['Добраться до площадки', 'Связаться с организаторами', 'Поделиться ботом'],
                                       ['Список докладов', 'Проголосовать за доклады','Результаты голосования'],
                                       ['Оценить организацию', 'Календарь событий', 'Об Ozon Tech']
                                       ], resize_keyboard=True
                                    )
    return my_keyboard

def send_photo(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/rick.jpg', 'rb'), reply_markup=get_keyboard())

def calendar(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    btn_site = [[InlineKeyboardButton('Мероприятия Ozon Tech', url='https://ozon.dev/events')]]
    reply_markup = InlineKeyboardMarkup(btn_site)
    update.message.reply_text('Тут можно узнать о ближайших событиях.', reply_markup = reply_markup)

def about(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    tech_about = [[InlineKeyboardButton('Об Ozon Tech', url='https://ozon.dev')]]
    reply_markup = InlineKeyboardMarkup(tech_about)
    update.message.reply_text('Тут можно узнать о технологиях.', reply_markup = reply_markup)

def contact(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    org_contact = 'Devrel OZON, Ани +7(968)123-45-67, telegram: @user'
    update.message.reply_text(org_contact, reply_markup=get_keyboard())

def subscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    if not user.get('subscribed'):
        toggle_subscription(db, user)
    context.bot.send_message(chat_id=update.message.chat_id, text='Я напомню о мероприятии через минуту.')
    context.job_queue.run_once(send_reminder, 2, context=update.message.chat_id)
    sub = 'Пользователь подписался на напоминание:'
    logging.info(sub)
    logging.info('User: %s, Chat id: %s', update.message.chat.username, update.message.chat.id)

def unsubscribe(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    if user.get('subscribed'):
        toggle_subscription(db, user)
        update.message.reply_text('Вы отписались от напоминаний.')
    else:
        update.message.reply_text('Вы не подписаны на напоминание, выполните /subscribe чтобы подписаться.')

#@mq.queuedmessage
def send_reminder(context):
    for user in get_subscribers(db):
        try:
            context.bot.send_message(chat_id=user['chat_id'], text='Напоминаю о мероприятии.')
        except error.BadRequest:
            print('Chat {} not found'.format(user['chat_id']))

def vote_for_reports(update, context):
    text = 'Проголосуйте за список докладов'
    inlinekbd = [[InlineKeyboardButton('1', callback_data='1'),
                    InlineKeyboardButton('2', callback_data='2'),
                    InlineKeyboardButton('3', callback_data='3'),
                    InlineKeyboardButton('4', callback_data='4'),
                    InlineKeyboardButton(emojize(':thumbs_up:'), callback_data='5')]]
    kdb_markup = InlineKeyboardMarkup(inlinekbd)
    update.message.reply_text(text)
    update.message.reply_text(list_of_reports.report_1, reply_markup=kdb_markup)
    update.message.reply_text(list_of_reports.report_2, reply_markup=kdb_markup)
    update.message.reply_text(list_of_reports.report_3, reply_markup=kdb_markup)

def vote_for_reports_pressed(update, context):
    query = update.callback_query
    print(update.callback_query.message.text)
    print(update.callback_query.data)
    save_vote_for_reports(db, update, update.callback_query, context, update.effective_user)
    text = 'Спасибо за ваш голос'

    vote = 'Пользователь проголосовал за доклады:'
    logging.info(vote)
    logging.info('User: %s, Chat id: %s', query.message.chat.username, query.message.chat.id)
    context.bot.edit_message_text(text=text, chat_id=query.message.chat.id, message_id=query.message.message_id)


def list_of_reports(update, context):
    report_1 = 'Первый доклад'
    report_2 = 'Второй доклад'
    report_3 = 'Третий доклад'
    update.message.reply_text(report_1, reply_markup=get_keyboard())
    update.message.reply_text(report_2, reply_markup=get_keyboard())
    update.message.reply_text(report_3, reply_markup=get_keyboard())

