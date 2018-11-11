import yaml
import requests
import pandas as pd
import pymorphy2
import nltk
from faq import get_faq_response
morph = pymorphy2.MorphAnalyzer()

composerDescriptions = yaml.load(open('composerDescriptions.yaml', 'r', encoding="utf-8"))
pavlovUrls = yaml.load(open('urls.yaml', 'r', encoding="utf-8"))
validComposers = ['рахманинов', 'чайковский']


def alice_info_endpoint(request, response, user_storage):
    composers = request.get_last_names(capitalize=False) & set(validComposers)

    word_tokens = request.get_tokens()
    if len(composers) == 1 or 'composer' in user_storage and 'он' in [morph.parse(word)[0].normal_form for word in word_tokens]:
        if len(composers) == 1:
            user_storage['composer'] = composers.pop()
            response.set_text(get_info(request.command, user_storage['composer']))
        else:
            for i, word in enumerate(word_tokens):
                if morph.parse(word)[0].normal_form == 'он':
                    word_tokens[i] = user_storage['composer']
            response.set_text(get_info(' '.join(word_tokens), user_storage['composer']))
        return response, user_storage
    response.set_text(get_faq_response(request.command))
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
    df[0] = df[0].apply(lambda word: morph.parse(word)[0].normal_form)
    df = df.loc[df[0].isin(validComposers)]
    #taking first composer
    if len(df) == 0:
        return None
    return df[0].iloc[0]
