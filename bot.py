import datetime, os, logging, sys
from threading import Thread

from telegram.ext import Updater, CommandHandler, ConversationHandler, \
    Filters, MessageHandler, RegexHandler, CallbackQueryHandler

from telegram.ext import messagequeue as mq

from handlers import *
from assessment import *
from reports import *
from db import *
import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='bot.log'
                    )

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=settings.PROXY)
    mybot.bot._msg_queue = mq.MessageQueue()
    mybot.bot._is_messages_queued_default = True

    logging.info('Бот запустился.')

    dp = mybot.dispatcher

    def stop_and_restart():
        mybot.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=stop_and_restart).start()
        logging.info('Бот перезагружен.')

    reports = ConversationHandler(
        entry_points = [
            MessageHandler(Filters.regex('^(Заполнить доклады)$'), start_create)
        ],
        states = {
            "report_1": [
                CommandHandler("cancel", cancel),
                MessageHandler(Filters.text, create_report_1)],
            "report_2": [
                CommandHandler("cancel", cancel),
                MessageHandler(Filters.text, create_report_2)],
            "report_3": [
                CommandHandler("cancel", cancel),
                MessageHandler(Filters.text, create_report_3)],
            "report_4": [
                CommandHandler("cancel", cancel),
                MessageHandler(Filters.text, create_report_4)],
            "report_5": [
                CommandHandler("cancel", cancel),
                MessageHandler(Filters.text, create_report_5)],
        },
        fallbacks=[MessageHandler(
            Filters.text | Filters.video | Filters.photo | Filters.document | Filters.location,
            dontknow_report
        )]
    )

    org_assessment = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Оценить организацию)$'), org_assessment_start, pass_user_data=True)],

        states={
            "name": [MessageHandler(Filters.text, org_assessment_get_name, pass_user_data=True)],
            "job": [MessageHandler(Filters.regex('^(0-1|1-2|2-5|5-10)$'), org_assessment_job, pass_user_data=True)],
            "poz": [MessageHandler(Filters.regex('^(Студент|Junior|Middle|Senior|TeamLead|Manager|Другое)$'), org_assessment_poz, pass_user_data=True)],
            "rating": [MessageHandler(Filters.regex('^(1|2|3|4|5|6|7|8|9|10)$'), org_assessment_rating, pass_user_data=True)],
            "comment": [MessageHandler(Filters.text, org_assessment_comment, pass_user_data=True),
                        CommandHandler('skip',org_assessment_comment_skip, pass_user_data=True)]
        },

        fallbacks=[MessageHandler(
            Filters.text | Filters.video | Filters.photo | Filters.document,
            dontknow,
            pass_user_data=True
        )]
    )

    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('r', restart, filters=Filters.user(username='@artivnv')))
    #dp.add_handler(CommandHandler('create', create_reports, filters=Filters.user(username='@artivnv')))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(reports)
    dp.add_handler(org_assessment)
    dp.add_handler(MessageHandler(Filters.regex('^(Добраться до площадки)$'), location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Связаться с организаторами)$'), contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Список докладов)$'), list_of_reports, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Проголосовать за доклады)$'), vote_for_reports, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(vote_for_reports_pressed))
    dp.add_handler(MessageHandler(Filters.regex('^(Результаты голосования)$'), send_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Поделиться ботом)$'), send_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Календарь событий)$'), calendar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Об Ozon Tech)$'), about, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.regex('^(От метро Выставочная)$'), location_vist, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(От метро Международная)$'), location_mejd, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(От МЦК Деловой центр)$'), location_mtsk, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.regex('^(Я на машине)$'), location_car, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.regex('^(Главное меню)$'), greet_user, pass_user_data=True))

    # Start
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()


