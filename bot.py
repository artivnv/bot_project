import os, logging, sys
from threading import Thread

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

from handlers import *
import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log'
                    )

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
        logging.info('Бот перезагружен.')

    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
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