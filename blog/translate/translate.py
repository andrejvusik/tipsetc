import json
import requests
import re
from flask import current_app
from flask_babel import _


def modify_text(text):
    pattern = r'[.!?] '
    return re.sub(pattern, '.', text)

def translate(source_language, dest_language, text):
    params = {
        'sl': source_language,
        'tl': dest_language,
        'q': modify_text(text),
        }
    #r = requests.get('https://translate.google.com/translate_a/single?client=at&dt=t&dt=ld&dt=qca&dt=rm&dt=bd&dj=1&hl=uk-RU&ie=UTF-8&oe=UTF-8&inputm=2&otf=2&iid=1dd3b944-fa62-4b55-b330-74909a99969e', params = params)
    r = requests.get(current_app.config['TRANSLATE_URL'], params = params)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    arr = json.loads(r.content.decode('utf-8-sig'))
    sentences = ''
    if arr['sentences']:
        for s in arr['sentences']:
            if s['trans']:
                sentences = sentences + s['trans']
                break
    return sentences
