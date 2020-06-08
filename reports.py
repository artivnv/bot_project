from telegram import ParseMode, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from db import db, save_reports

def start_create(update, context):
    update.message.reply_text(
        'Введи название первого доклада или /cancel чтоб сохранить и выйти из заполнения.',
        reply_markup = ReplyKeyboardRemove()
    )
    return "report_1"

def create_report_1(update, context):
    context.user_data['report_1'] = update.message.text
    update.message.reply_text(
        'Введи название второго доклада или /cancel чтоб сохранить и выйти из заполнения.',
        reply_markup = ReplyKeyboardRemove()
    )
    return "report_2"

def create_report_2(update, context):
    context.user_data['report_2'] = update.message.text
    update.message.reply_text(
        'Введи название третьего доклада или /cancel чтоб сохранить и выйти из заполнения.',
        reply_markup = ReplyKeyboardRemove()
    )
    return "report_3"

def create_report_3(update, context):
    context.user_data['report_3'] = update.message.text
    update.message.reply_text(
        'Введи название четвертого доклада или /cancel чтоб сохранить и выйти из заполнения.',
        reply_markup = ReplyKeyboardRemove()
    )
    return "report_4"

def create_report_4(update, context):
    context.user_data['report_4'] = update.message.text
    update.message.reply_text(
        'Введи название пятого доклада или /cancel чтоб сохранить и выйти из заполнения.',
        reply_markup = ReplyKeyboardRemove()
    )
    return "report_5"

def create_report_5(update, context):
    context.user_data['report_5'] = update.message.text
    save_reports(db, update.effective_user, context.user_data)
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text('Вышли из заполнения')
    return ConversationHandler.END

def dontknow_report(update, context):
    update.message.reply_text('Не понимаю.')