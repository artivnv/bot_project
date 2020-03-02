import logging
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
level=logging.INFO,
filename='bot.log')

PROXY = {'proxy_url': 'socks5://t3.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(bot, update):
    text = 'Вызвана команда start'
    print(text)
    update.message.reply_text(text)

def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def main():
    with open('token.txt') as f:
        TOKEN = f.read().strip()
    mybot = Updater(TOKEN, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    mybot.start_polling()
    mybot.idle()
if __name__ == "__main__":
    main()
