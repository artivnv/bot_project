Event_Bot
========

Event_Bot - это Telegram бот для организаторов it-мероприятий с подключенной к нему
административной панелью на базе `Flask-Admin`_.
Библиотека для работы с ботом `python-telegram-bot`_.

Event_Bot is a Telegram bot for organizers of it-events with it connected
admin panel based on `Flask-Admin`_.
Library for working with the bot `python-telegram-bot`_.

Установка/Installing
----------

Создайте виртуальное окружение и активируйте его. В виртуальном окружении выполните:

.. code-block:: text

    pip install -r requirements.txt

Настройка/
----------

Создайте файл settings.py по следующему примеру:

.. code-block:: python

    PROXY = {'proxy_url': 'socks5h://SOCKS5H_PROXY:1080',
        'urllib3_proxy_kwargs': {'username': 'LOGIN', 'password': 'PASSWORD'}}

    API_KEY = 'API ключ'

Запуск/
-------

В активированном виртуальном окружении выполните:

.. code-block:: text

    python3 bot.py




.. _Flask-Admin: https://github.com/flask-admin/flask-admin
.. _python-telegram-bot: https://github.com/python-telegram-bot/python-telegram-bot