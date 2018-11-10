import datetime
import humanize
import coloredlogs, logging
coloredlogs.install()

from answers import get_replica
from playbill import find_concerts
from alice_sdk import AliceRequest, AliceResponse
from common import right_form_from_number, BuyStatus

humanize.i18n.activate('ru_RU')

logging.basicConfig(level=logging.DEBUG)

composers = {"Рахманинов", "Чайковский", "Свиридов"}

date_variants = ["в следующем месяце", "в декабре"]


def send_response(response, user_storage, tag, add_variants=True):
    answer_text = get_replica(tag)
    response.set_text(answer_text)
    if add_variants:
        response.set_variants(*composers, *date_variants)
    return response, user_storage


def book(request: AliceRequest, response: AliceResponse, user_storage):
    if not user_storage.get('buy-status'):
        user_storage["buy-status"] = BuyStatus.Choosing
        user_storage["composers"] = composers.copy()
        return send_response(response, user_storage, "select-concert")

    if user_storage.get('buy-status') == BuyStatus.Selected:
        user_storage.pop('buy-status')
        return send_response(
            response, user_storage, 'concert-selected', add_variants=False)

    last_names = request.get_last_names()

    if len(last_names):
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
        logging.error('has dates')
        dates = request.get_date()
        start = dates[0]
        if 'month_is_relative' in start:
            if start['month_is_relative'] == False:
                logging.error('relative')
            else:
                logging.error('non relative')                

    logging.debug(f"start date: {humanize.naturaltime(start_date)}")

    concerts = find_concerts(user_storage['composers'], start_date, end_date)

    if concerts.empty:
        return send_response(response, user_storage, 'select-concert-empty')
    logging.info(f"found: {concerts.shape[1]} concerts")

    text = f"{'Нашлось' if len(concerts) > 1 else 'Нашёлся'} {len(concerts)} {right_form_from_number('концерт', len(concerts))}. Скажи номер понравившегося!\n"
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

    response.set_text(text)
    response.set_buttons(buttons)
    user_storage["buy-status"] = BuyStatus.Selected
    return response, user_storage
