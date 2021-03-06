# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

import logging
from urllib.parse import unquote

# Импортируем модули для работы с логами.
import coloredlogs
import nltk
import pymorphy2
# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

# Импортируем модуль для работы с API Алисы
from alice_sdk import AliceRequest, AliceResponse
# Импортируем модуль с логикой игры
from dialogs import handle_dialog
from info import get_info, get_composers
from faq import get_faq_response
from playbill import get_all_playbill

coloredlogs.install()



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
    word_tokens = nltk.word_tokenize(text.lower())
    morph = pymorphy2.MorphAnalyzer()
    word_normal_forms = [morph.parse(word)[0].normal_form for word in word_tokens]
    composer = get_composers(word_tokens)
    global composerContext

    if any(keyword in word_normal_forms for keyword in ["афиша", "расписание"]):
        if composer:
            return get_all_playbill([composer.capitalize()], to_json=False)
        else:
            return get_all_playbill(to_json=False)

    if composer or request.json['id'] in list(composerContext.keys()) and 'он'\
            in word_normal_forms:
        if composer:
            composerContext[request.json['id']] = composer
        else:
            composer = composerContext[request.json['id']]
            for i in range(len(word_tokens)):
                if word_normal_forms[i] == 'он':
                    word_tokens[i] = composer
            text = " ".join(word_tokens)
        return get_info(text, composer)
    composerContext.pop(request.json['id'], None)
    logging.info(f"composer not found")
    return get_faq_response(text)

@app.route("/playbill")
def get_playbill():
    composer = request.args.get('composer')
    if composer:
        composer = unquote(composer)
    if composer not in ["Чайковский", "Рахманинов", "Свиридов"]:
        return get_all_playbill()
    return get_all_playbill([composer])

if __name__ == '__main__':
    app.run()
