import datetime
import logging
from calendar import monthrange

import coloredlogs
import humanize

from alice_sdk import AliceRequest, AliceResponse
from answers import get_replica
from common import BuyStatus, last_day_in_month, right_form_from_number
from playbill import find_concerts

coloredlogs.install()

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
    if not user_storage.get("buy-status"):
        user_storage["buy-status"] = BuyStatus.Choosing
        user_storage["composers"] = composers.copy()
        return send_response(response, user_storage, "select-concert")

    if user_storage.get("buy-status") == BuyStatus.Selected:
        user_storage.pop("buy-status")
        return send_response(
            response, user_storage, "concert-selected", add_variants=False
        )

    last_names = request.get_last_names()

    if len(last_names):
        user_storage["composers"] &= last_names

    logging.debug(f"Composers for request {' '.join(user_storage['composers'])}")

    if len(user_storage["composers"]) == 0:
        user_storage["composers"] = composers.copy()
        return send_response(response, user_storage, "select-concert-composer-unknown")

    # I'm really feel sorry for this code
    # but working with time sucks
    # working with time ranges sucks twice

    start_date = datetime.date.today()
    end_date = None
    if request.has_date():
        logging.debug("has dates")
        dates = request.get_date()
        start = dates[0]
        if "month_is_relative" in start:
            month = None
            if start["month_is_relative"] == True:
                month_add = start["month"]
                if month_add < 0:
                    return send_response(response, user_storage, "select-concert-empty")
                month = max(1, (datetime.date.today().month + month_add) % 13)
                logging.debug("relative time")
            else:
                month = start["month"]
                logging.debug("non relative time")
            if month in [11, 12]:
                start_date = datetime.date(2018, month, 1)
            elif month < 5:
                start_date = datetime.date(2019, month, 1)
            else:
                return send_response(response, user_storage, "select-concert-empty")
            end_date = last_day_in_month(start_date)

    start_date = max(start_date, datetime.date.today())
    logging.debug(f"start date: {humanize.naturalday(start_date)}")
    if end_date:
        logging.debug(f"end date: {humanize.naturalday(end_date)}")

    concerts = find_concerts(user_storage["composers"], start_date, end_date)

    if concerts.empty:
        return send_response(response, user_storage, "select-concert-empty")
    logging.info(f"found: {concerts.shape[0]} concerts")

    text = f"{'Нашлось' if len(concerts) > 1 else 'Нашёлся'} {len(concerts)} {right_form_from_number('концерт', len(concerts))}. Скажи номер понравившегося!\n"
    buttons = []

    for i, (_, concert) in enumerate(concerts.iterrows()):
        i += 1
        day = concert["дата, гггг-мм-дд"]
        buttons.append({"title": str(i), "url": concert["купить билет"], "hide": True})
        text += f"\n{i}. {concert['title']}, {day.day}.{day.month}.{day.year}"

    response.set_text(text)
    response.set_buttons(buttons)
    user_storage["buy-status"] = BuyStatus.Selected
    return response, user_storage
