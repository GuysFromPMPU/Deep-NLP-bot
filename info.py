import yaml
import requests
import pandas as pd
import pymorphy2
import nltk
from faq import get_faq_response

import coloredlogs, logging
coloredlogs.install()


morph = pymorphy2.MorphAnalyzer()

composerDescriptions = yaml.load(open('composerDescriptions.yaml', 'r', encoding="utf-8"))
pavlovUrls = yaml.load(open('urls.yaml', 'r', encoding="utf-8"))
validComposers = ['рахманинов', 'чайковский', 'бузов']


def alice_info_endpoint(request, response, user_storage):
    composers = request.get_last_names(capitalize=False) & set(validComposers)

    word_tokens = request.get_tokens()
    word_normal_forms = [morph.parse(word)[0].normal_form for word in word_tokens]
    if len(composers) == 1 or 'composer' in user_storage and 'он' in word_normal_forms:
        if len(composers) == 1:
            user_storage['composer'] = composers.pop()
            response.set_text(get_info(request.command, user_storage['composer']))
        else:
            for i in range(len(word_tokens)):
                if word_normal_forms[i] == 'он':
                    word_tokens[i] = user_storage['composer']
            response.set_text(get_info(' '.join(word_tokens), user_storage['composer']))
        return response, user_storage

    user_storage.pop('composer', None)
    response.set_text(get_faq_response(request.command))
    return response, user_storage

def get_info(request, composer="чайковский"):
    logging.error(f"get info from composer command: {request}")
    r = requests.post(pavlovUrls['squad_path'], json={
        'context': composerDescriptions[composer],
        'question': [request]
    })
    return r.json()[0][0]


#ATTENTION!!! DEPRECATED! USE IT ON YOUR OWN RISK!
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

def get_composers(tokenizedText):
    composers = [morph.parse(word)[0].normal_form for word in tokenizedText
                 if morph.parse(word)[0].normal_form in validComposers]
    return composers[0] if len(composers) > 0 else None
