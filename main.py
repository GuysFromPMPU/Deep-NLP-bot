# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с логами.
import coloredlogs, logging
coloredlogs.install()
import pymorphy2
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

import nltk

app = Flask(__name__)
app.config['TESTING'] = True

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
session_storage = {}

composerContext = {}

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
    global composerContext
    morph = pymorphy2.MorphAnalyzer()
    word_tokens = nltk.word_tokenize(text.lower())
    if composer or request.json['id'] in list(composerContext.keys()) and 'он'\
            in [morph.parse(word)[0].normal_form for word in word_tokens]:
        if composer:
            composerContext[request.json['id']] = composer
        else:
            composer = composerContext[request.json['id']]
            for idx, word in enumerate(word_tokens):
                if morph.parse(word)[0].normal_form == 'он':
                    word_tokens[idx] = composer
            text = " ".join(word_tokens)
        return get_info(text, composer)
    composerContext.pop(request.json['id'], None)
    logging.info(f"composer not found")
    return get_faq_response(text)

@app.route("/playbill")
def get_playbill():
    return get_all_playbill()

if __name__ == '__main__':
    app.run()
