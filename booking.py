import logging

from answers import get_replica
from playbill import find_concerts

logging.basicConfig(level=logging.DEBUG)

composers = {"Рахманинов", "Чайковский"}

date_variants = ["в следующем месяце", "в декабре"]


def send_response(response, user_storage, tag):
    unknown_text = get_replica(tag)
    response.set_text(unknown_text)
    response.set_variants(*composers, *date_variants)
    return response, user_storage


def book(request, response, user_storage):
    user_storage.setdefault("buying", True)
    user_storage.setdefault("composers", composers.copy())
    logging.error(f"\n\n\n{' '.join(user_storage['composers'])}\n\n\n")

    if not user_storage.setdefault('asked', False):
        user_storage["asked"] = True
        return send_response(response, user_storage, "select-concert")

    last_names = [
        fio.get("last_name", "").capitalize() for fio in request.get_fio()
    ]
    last_names = set(filter(None, last_names))

    user_storage['composers'] &= last_names

    if len(user_storage['composers']) == 0:
        user_storage['composers'] = composers.copy()
        return send_response(response, user_storage,
                             'select-concert-composer-unknown')

    date = None
    if request.has_date():
        date = request.get_date()[0]

    concerts = find_concerts(user_storage['composers'], date)
    if not concerts:
        return send_response(response, user_storage, 'select-concert-empty')

    response.set_text(str('\n\n\n'.join(concerts["title"])))
    return response, user_storage

    if not user_storage["composer"]:
        for composer in composers:
            if (request.has_lemmas(composer)):
                user_storage["composer"] = composer
                break
        #else:
        #return select_concert(response, user_storage)

    response.set_text(f"Ты выбрал {user_storage['composer']}")

    return response, user_storage
