import logging
import os

from telegram import ReplyKeyboardMarkup, \
    InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, error
from telegram.ext import messagequeue as mq

from db import db, get_or_create_user, toggle_subscription, get_subscribers

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

def location(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    navigation_text = 'Выбери откуда тебе удобно добраться. Самый близкий маршрут от станции метро «Международная».'
    update.message.reply_text(navigation_text, reply_markup=get_keyboard_1())

def get_keyboard_1():
    my_keyboard_1 = ReplyKeyboardMarkup([
                                        ['От метро Выставочная', 'От метро Международная'],
                                        ['От МЦК Деловой центр', 'Я на машине'],
                                        ['Главное меню']
                                        ], resize_keyboard=True
                                    )
    return my_keyboard_1

def location_vist(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    update.message.reply_text('''
<b>Адрес офиса Ozon: Москва, Пресненская наб.,10, БЦ “Башня на набережной” блок С, этаж 30</b>
<b>Важно! При себе нужно иметь документ, удостоверяющий личность (паспорт, водительское удостоверение).</b>

<pre>Выставочная</pre>
''', parse_mode=ParseMode.HTML)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/scheme.png', 'rb'), reply_markup=get_keyboard())

def location_mejd(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    update.message.reply_text('''
<b>Адрес офиса Ozon: Москва, Пресненская наб. 10, БЦ “Башня на набережной” блок С, этаж 30</b>
<b>Важно! При себе нужно иметь документ, удостоверяющий личность (паспорт, водительское удостоверение).</b>

<pre>Международная
- Предпоследний вагон из центра, выход в сторону IQ-квартала и ТРЦ «Афимолл сити»
- Далее поднимайтесь по двум эскалаторам подряд (вы окажетесь в IQ квартале)
- Поднявшись, поверните налево в сторону выхода с рамками-металлоискателями
- На выходе оказываетесь напротив БЦ «Башни на набережной»(слева от вас будет гостиница Novotel)
- Вам останется перейти дорогу и зайти в ближайший блок С</pre>
''', parse_mode=ParseMode.HTML)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/scheme.png', 'rb'), reply_markup=get_keyboard())

def location_mtsk(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    update.message.reply_text('''
<b>Адрес офиса Ozon: Москва, Пресненская наб.,10, БЦ “Башня на набережной” блок С, этаж 30</b>
<b>Важно! При себе нужно иметь документ, удостоверяющий личность (паспорт, водительское удостоверение).</b>

<pre>МЦК</pre>

''', parse_mode=ParseMode.HTML)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/scheme.png', 'rb'), reply_markup=get_keyboard())

def location_car(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    update.message.reply_text('''
<b>Адрес офиса Ozon: Москва, Пресненская наб.,10, БЦ “Башня на набережной” блок С, этаж 30</b>
<b>Важно! При себе нужно иметь документ, удостоверяющий личность (паспорт, водительское удостоверение).</b>

<pre>Вы можете добраться на своем транспорте, для этого необходимо заранее сообщить организаторам ГОС номер автомобиля.
Заезд со стороны набережной. Рядом с КПП указатель “Naberezhnaya Tower”.</pre>
''', parse_mode=ParseMode.HTML)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/scheme.png', 'rb'), reply_markup=get_keyboard())

def send_photo(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/rick.jpg', 'rb'), reply_markup=get_keyboard())

def send_scheme(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/scheme.png', 'rb'), reply_markup=get_keyboard())

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
    org_contact = 'Devrel OZON, Ани +7(968)381-56-10, telegram: @step_ani'
    update.message.reply_text(org_contact, reply_markup=get_keyboard())

#def talk_to_me(bot, update):
#    user_text = (update.message.chat.first_name, update.message.text)
#    logging.info('User: %s, Chat id: %s, Message: %s', update.message.chat.username,
#                 update.message.chat.id, update.message.text)
#    update.message.reply_text(user_text, reply_markup=get_keyboard())


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






