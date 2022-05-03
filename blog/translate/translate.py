import json
import requests
from flask import current_app
from flask_babel import _

def translate(source_language, dest_language, text):
    params = {
        'sl': source_language,
        'tl': dest_language,
        'q': text,
        }
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
