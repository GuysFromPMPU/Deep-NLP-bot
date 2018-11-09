import re

import json
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


class AliceRequest(object):
    def __init__(self, request_dict):
        self._request_dict = request_dict
        self._command = request_dict['request']['command'].rstrip('.')
        self._words = re.findall(r'[\w-]+', self._command, flags=re.UNICODE)
        self._lemmas = [morph.parse(word)[0].normal_form
                        for word in self._words]

    @property
    def version(self):
        return self._request_dict['version']

    @property
    def session(self):
        return self._request_dict['session']

    @property
    def user_id(self):
        return self.session['user_id']

    @property
    def is_new_session(self):
        return bool(self.session['new'])
    
    @property
    def command(self):
        return self._request_dict['request']['command']

    def __str__(self):
        return str(self._request_dict)

    def has_lemmas(self, *lemmas):
        return any(morph.parse(item)[0].normal_form in self._lemmas
                   for item in lemmas)
    

class AliceResponse(object):
    def __init__(self, alice_request):
        self._response_dict = {
            "version": alice_request.version,
            "session": alice_request.session,
            "response": {
                "end_session": False
            }
        }

    def dumps(self):
        return json.dumps(
            self._response_dict,
            ensure_ascii=False,
            indent=2
        )

    def set_text(self, text):
        self._response_dict['response']['text'] = text[:1024]

    def set_buttons(self, buttons):
        self._response_dict['response']['buttons'] = buttons

    def set_end_session(self, flag):
        self._response_dict['response']['end_session'] = flag

    def __str__(self):
        return self.dumps()