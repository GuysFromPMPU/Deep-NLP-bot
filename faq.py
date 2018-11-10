import recastai
from answers import get_replica
import random

build = recastai.Build('bc3c523dc4d9eb759ed94d7f8355e69a', 'ru')

def get_faq_response(content):
    response = build.dialog({'type': 'text', 'content': content}, random.randint(1, 101))
    if response.nlp.intents[0].confidence < 0.98:
        return get_replica('undefined')
    return response.messages[0].content

