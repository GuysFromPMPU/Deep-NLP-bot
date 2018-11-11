import operator
import datetime

import pandas as pd

tea = pd.read_csv(open("Концерты Чайковский.csv", 'r', encoding='utf-8'), encoding="utf-8", parse_dates=[1, 2])
rah = pd.read_csv(open("Концерты_Рахманинов.csv", 'r', encoding='utf-8'), encoding="utf-8", parse_dates=[1, 2])
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

    finded = finded[finded['программа'].str.contains('|'.join(composers))]
    
    return finded#.to_dict(orient="list")

def get_all_playbill(composer):
    finded = find_concerts([composer])
    return finded.to_json(orient='records', force_ascii=False)

# print(find_concerts(["Свиридов", "Чайковский"], datetime.datetime(2019, 2, 24, 0, 0)))
