import logging
import os
import sys
from threading import Thread

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, RegexHandler

import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log'
                    )

def greet_user(update, context):
    text = 'Вызван старт'
    logging.info(text)
    bot_text = 'Привет, я бот помощник.'
    update.message.reply_text(bot_text, reply_markup=get_keyboard())

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([
                                       ['Добраться до площадки', 'Связаться с организаторами', 'Список докладов'],
                                       ['Проголосовать за доклады','Посмотреть результаты голосования'],
                                       ['Поделиться ботом', 'Календарь событий', 'Об Ozon Tech']
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

def send_photo(update, context):
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/rick.jpg', 'rb'), reply_markup=get_keyboard())

def talk_to_me(bot, update):
    user_text = (update.message.chat.first_name, update.message.text)
    logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=settings.PROXY)
    logging.info('Бот запустился.')
    dp = mybot.dispatcher

    def stop_and_restart():
        mybot.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()
        logging.info('Перезапуск.')

    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    #dp.add_handler(CommandHandler('send', send_photo, pass_user_data=True))
    dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username='@artivnv')))
    dp.add_handler(MessageHandler(Filters.regex('^(Добраться до площадки)$'), location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Связаться с организаторами)$'), send_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Список докладов)$'), send_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Проголосовать за доклады)$'), send_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Посмотреть результаты голосования)$'), send_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Поделиться ботом)$'), send_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Календарь событий)$'), calendar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Об Ozon Tech)$'), about, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(От метро Выставочная)$'), location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(От метро Международная)$'), location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(От МЦК Деловой центр)$'), location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Я на машине)$'), location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Главное меню)$'), greet_user, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    # Start
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()