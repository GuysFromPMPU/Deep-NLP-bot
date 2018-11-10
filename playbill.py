import operator
import datetime

import pandas as pd

tea = pd.read_csv(open("Концерты Чайковский.csv", 'r', encoding='utf-8'), encoding="utf-8", parse_dates=[1, 2])
rah = pd.read_csv(open("Концерты_Рахманинов.csv", 'r', encoding='utf-8'), encoding="utf-8", parse_dates=[1, 2])
res = pd.concat([tea, rah])
res["дата, гггг-мм-дд"] = pd.to_datetime(res["дата, гггг-мм-дд"])


def find_concerts(composers, start_date=None, end_date=None):
    global res
    if start_date is None:
        start_date = pd.to_datetime('today')

    res = res[res["дата, гггг-мм-дд"] >= start_date]
    if end_date:
        res = res[res["дата, гггг-мм-дд"] <= end_date]

    res = res[res['программа'].str.contains('|'.join(composers))]
    return res.to_dict(orient="list")

print(find_concerts(["Свиридов", "Чайковский"], datetime.datetime(2019, 2, 24, 0, 0)))
