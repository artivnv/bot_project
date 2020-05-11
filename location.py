from telegram import ReplyKeyboardMarkup, ParseMode

from db import db, get_or_create_user

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

def send_scheme(update, context):
    user = get_or_create_user(db, update.effective_user, update.message)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=open('images/scheme.png', 'rb'), reply_markup=get_keyboard())

