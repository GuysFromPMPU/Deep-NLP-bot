# coding: utf-8
from __future__ import unicode_literals

from answers import get_replica
from booking import book
from common import ChatStatus
from info import alice_info_endpoint


# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        user_storage = {}
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его
        hello_text = get_replica("newcomer-hello")
        response.set_text(hello_text)
        response.set_variants("Узнать афишу", "Ответы на часто задаваемые вопросы")
        return response, user_storage

    if request.has_lemmas("билет", "афиша", "купить", "расписание") or user_storage.get("buying") == True:
        return book(request, response, user_storage)
    return alice_info_endpoint(request, response, user_storage)

    # Обрабатываем ответ пользователя.
    if request.command.lower() in ['ладно', 'куплю', 'покупаю', 'хорошо']:
        # Пользователь согласился, прощаемся.
        response.set_text('Слона можно найти на Яндекс.Маркете!')

        return response, user_storage

    # Если нет, то убеждаем его купить слона!
    #buttons, user_storage = get_suggests(user_storage)
    response.set_text('Все говорят "{}", а ты купи слона!'.format(
        request.command))
    #response.set_buttons(buttons)

    return response, user_storage


# Функция возвращает две подсказки для ответа.
def get_suggests(user_storage):
    # Выбираем две первые подсказки из массива.
    suggests = [{
        'title': suggest,
        'hide': True
    } for suggest in user_storage['suggests'][:2]]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    user_storage['suggests'] = user_storage['suggests'][1:]

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests, user_storage
