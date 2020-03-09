from glob import glob
import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, RegexHandler

import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update):
    text = 'Вызван старт'
    logging.info(text)
    bot_text = 'Привет, я бот помощник.'
    my_keyboard = ReplyKeyboardMarkup([
                                       ['Как добраться до площадки']
    #                                  ['Посмотреть расписание докладов'],
    #                                  ['Проголосовать за доклады'],
    #                                  ['Посмотреть результаты голосования'],
    #                                  ['Связаться с организаторами'],
    #                                  ['Поделиться ботом'],
    #                                  ['Посмотреть календарь событий']
                                       ]
                                    )
    update.message.reply_text(bot_text, reply_markup=get_keyboard())

def talk_to_me(bot, update):
    user_text = (update.message.chat.first_name, update.message.text)
    logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username,
                 update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())

def send_location(bot, update):
    send_pic = glob('images/rick.jp*g')
    bot.send_photo(chat_id=update.message.chat.id, photo=open(send_pic, 'rb'), reply_markup=get_keyboard())

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([
                                       ['Как добраться до площадки']
    #                                  ['Посмотреть расписание докладов'],
    #                                  ['Проголосовать за доклады'],
    #                                  ['Посмотреть результаты голосования'],
    #                                  ['Связаться с организаторами']
    #                                  ['Поделиться ботом'],
    #                                  ['Посмотреть календарь событий']
                                       ], resize_keyboard=True
                                    )
    return my_keyboard

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=settings.PROXY)
    logging.info('Бот запустился.')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('send', send_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Как добраться до площадки)$', send_location, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Посмотреть расписание докладов)$', send_location, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(Проголосовать за доклады)$', send_location, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(Посмотреть результаты голосования)$', send_location, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(Связаться с организаторами)$', send_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()

main()
