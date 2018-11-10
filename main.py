# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с логами.
import coloredlogs, logging
coloredlogs.install()
import random

import yaml
# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

# Импортируем модуль для работы с API Алисы
from alice_sdk import AliceRequest, AliceResponse
# Импортируем модуль с логикой игры
from dialogs import handle_dialog
from info import get_info, get_ner
from answers import get_replica
from faq import get_faq_response
from playbill import get_all_playbill

app = Flask(__name__)
app.config['TESTING'] = True

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
session_storage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    alice_request = AliceRequest(request.json)
    logging.info('Request: {}'.format(alice_request))

    alice_response = AliceResponse(alice_request)

    user_id = alice_request.user_id

    alice_response, session_storage[user_id] = handle_dialog(
        alice_request, alice_response, session_storage.get(user_id))

    logging.info('Response: {}'.format(alice_response))

    return alice_response.dumps()

@app.route("/textProcessing", methods=['POST'])
def processText():
    text = request.json['request']
    logging.info(f"text to answer: {text}")
    composer = get_ner(text)
    if not composer:
        logging.info(f"composer not found")
        return get_faq_response(text)
    return get_info(text, composer)

@app.route("/playbill")
def get_playbill():
    return get_all_playbill()

if __name__ == '__main__':
    app.run()
