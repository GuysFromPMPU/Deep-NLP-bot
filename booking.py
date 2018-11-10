import datetime
import humanize
import coloredlogs, logging
coloredlogs.install()

from answers import get_replica
from playbill import find_concerts
from alice_sdk import AliceRequest, AliceResponse
from common import right_form_from_number


humanize.i18n.activate('ru_RU')

logging.basicConfig(level=logging.NOTSET)

composers = {"Рахманинов", "Чайковский", "Свиридов"}

date_variants = ["в следующем месяце", "в декабре"]


def send_response(response, user_storage, tag):
    unknown_text = get_replica(tag)
    response.set_text(unknown_text)
    response.set_variants(*composers, *date_variants)
    return response, user_storage


def book(request : AliceRequest, response : AliceResponse, user_storage):
    user_storage["buying"] = True

    if not user_storage.get('asked'):
        user_storage["asked"] = True
        user_storage["composers"] = composers.copy()
        return send_response(response, user_storage, "select-concert")

    last_names = request.get_last_names()

    user_storage['composers'] &= last_names

    logging.debug(
        f"Composers for request {' '.join(user_storage['composers'])}")

    if len(user_storage['composers']) == 0:
        user_storage['composers'] = composers.copy()
        return send_response(response, user_storage,
                             'select-concert-composer-unknown')

    start_date = datetime.date.today()
    end_date = None
    if request.has_date():
        dates = request.get_date()


    logging.debug(f"start date: {humanize.naturaltime(start_date)}")

    concerts = find_concerts(user_storage['composers'], start_date, end_date)

    if concerts.empty:
        return send_response(response, user_storage, 'select-concert-empty')

    text = f"{'Нашлось' if len(concerts) > 1 else 'Нашелся'} {len(concerts)} {right_form_from_number('концерт', len(concerts))}. Скажи номер понравившегося!\n"
    buttons = []

    humanize.i18n.activate('ru_RU')

    for i, (_, concert) in enumerate(concerts.iterrows()):
        i += 1
        buttons.append({
            "title": str(i),
            "url": concert["купить билет"],
            "hide": True
        })
        text += f"\n{i}. {concert['title']}, {humanize.naturaltime(concert['дата, гггг-мм-дд'])}"

    logging.info(f"\n\nfound: {len(concerts['title'])}\n\n")
    response.set_text(text)
    response.set_buttons(buttons)
    return response, user_storage
