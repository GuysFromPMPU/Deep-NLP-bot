import datetime
import logging

import coloredlogs
import pandas as pd

from common import right_form_from_number

coloredlogs.install()
logging.basicConfig(level=logging.DEBUG)


tea = pd.read_csv(
    open("Концерты Чайковский.csv", "r", encoding="utf-8"),
    encoding="utf-8",
    parse_dates=[1, 2],
)
rah = pd.read_csv(
    open("Концерты_Рахманинов.csv", "r", encoding="utf-8"),
    encoding="utf-8",
    parse_dates=[1, 2],
)
res = pd.concat([tea, rah])
res["дата, гггг-мм-дд"] = pd.to_datetime(res["дата, гггг-мм-дд"]).dt.date
res.sort_values(by=["дата, гггг-мм-дд"], inplace=True)


def find_concerts(composers, start_date=None, end_date=None):
    finded = res.copy()
    if start_date is None:
        start_date = datetime.date.today()

    finded = finded[finded["дата, гггг-мм-дд"] >= start_date]
    if end_date:
        finded = finded[finded["дата, гггг-мм-дд"] <= end_date]

    finded = finded[finded["программа"].str.contains("|".join(composers))]

    return finded


def get_all_playbill(composer=["Чайковский", "Рахманинов", "Свиридов"], to_json=True):
    logging.error(f"request info for {' '.join(composer)}")
    finded = find_concerts(composer)
    logging.error(f"number of finded concerts {finded.shape[0]}")
    if to_json:
        return finded.to_json(orient="records", force_ascii=False)
        
    finded = finded.head(3)
    text = f"{'Нашлось' if len(finded) > 1 else 'Нашёлся'} {len(finded)} {right_form_from_number('ближайших', len(finded))} {right_form_from_number('концерт', len(finded))}\n"
    for i, (_, concert) in enumerate(finded.iterrows()):
        i += 1
        day = concert["дата, гггг-мм-дд"]
        text += f"\n{i}. {concert['title']}, {day.day}.{day.month}.{day.year}"
    logging.error(text)
    return text


# print(find_concerts(["Свиридов", "Чайковский"], datetime.datetime(2019, 2, 24, 0, 0)))
