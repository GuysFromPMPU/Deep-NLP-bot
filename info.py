import yaml
import requests

composerDescriptions = yaml.load(open('composerDescriptions.yaml', 'r', encoding="utf-8"))
pavlovUrls = yaml.load(open('urls.yaml', 'r', encoding="utf-8"))

composers_texts = {
    'Чайковский': composerDescriptions['Чайковский'],
    'Рахманинов': composerDescriptions['Рахманинов']
}

def alice_info_endpoint(request, response, user_storage, composer="Чайковский"):
    response.set_text(get_info(request, composer))
    return response, user_storage

def get_info(request, composer="Чайковский"):
    r = requests.post(pavlovUrls['squad_path'], json={
        'context': composerDescriptions[composer],
        'question': [request]
    })
    return r.json()[0][0]

