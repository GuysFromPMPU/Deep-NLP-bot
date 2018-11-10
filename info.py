import yaml
import requests
import pandas as pd
import pymorphy2
from answers import get_replica
morph = pymorphy2.MorphAnalyzer()

composerDescriptions = yaml.load(open('composerDescriptions.yaml', 'r', encoding="utf-8"))
pavlovUrls = yaml.load(open('urls.yaml', 'r', encoding="utf-8"))
validComposers = ['рахманинов', 'чайковский']

composers_texts = {
    'чайковский': composerDescriptions['чайковский'],
    'рахманинов': composerDescriptions['рахманинов']
}

def alice_info_endpoint(request, response, user_storage):
    composer = get_ner(request.command)
    if composer is None:
        response.set_text(get_replica('undefined'))
        return response, user_storage
        
    response.set_text(get_info(request, composer))

    return response, user_storage

def get_info(request, composer="чайковский"):
    r = requests.post(pavlovUrls['squad_path'], json={
        'context': composerDescriptions[composer],
        'question': [request]
    })
    return r.json()[0][0]

def get_ner(request):
    r = requests.post(pavlovUrls['ner_path'], json={
        'context': [request]
    })
    df = pd.DataFrame.from_records(r.json()[0]).transpose()
    if len(df) == 0:
        return None
    df = df[df[1] != 'O']
    #Get persons from text
    df = df[df[1].str.contains("PER", na=False)]
    df[0] = df[df[1] == "B-PER"][0].apply(lambda word: morph.parse(word)[0].normal_form)
    df = df.loc[df[0].isin(validComposers)]
    #taking first composer
    if len(df) == 0:
        return None
    return df[0].iloc[0]
