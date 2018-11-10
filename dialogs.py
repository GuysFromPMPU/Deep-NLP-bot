from answers import get_replica
from booking import book
from info import alice_info_endpoint


# Функция для непосредственной обработки диалога.
def handle_dialog(request, response, user_storage):
    if request.is_new_session:
        user_storage = {}
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его
        hello_text = get_replica("newcomer-hello")
        response.set_text(hello_text)
        response.set_variants("Узнать афишу", "Время работы", "Где родился Чайковский?")
        return response, user_storage

    if request.has_lemmas("билет", "афиша", "купить", "расписание") or user_storage.get('buy-status'):
        return book(request, response, user_storage)

    return alice_info_endpoint(request, response, user_storage)
