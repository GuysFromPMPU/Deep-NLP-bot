import operator
import datetime

import pandas as pd

tea = pd.read_csv(open("Концерты Чайковский.csv", 'r', encoding='utf-8'), encoding="utf-8", parse_dates=[1,2])
rah = pd.read_csv(open("Концерты_Рахманинов.csv", 'r', encoding='utf-8'), encoding="utf-8", parse_dates=[1,2])
res = pd.concat([tea, rah])
#print(pd.to_datetime(res["дата, гггг-мм-дд"]).head())

res["дата, гггг-мм-дд"] = pd.to_datetime(res["дата, гггг-мм-дд"])
#res["время, чч-мм"] = pd.to_datetime(res["время, чч-мм"] )

print(res.dtypes)

def find_concerts(composers, date=None):
    op = operator.ge if date == None else operator.eq
    if date == None:
        date = pd.to_datetime('today')
    
    res["дата, гггг-мм-дд"]

    return None