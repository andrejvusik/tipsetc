from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length, Optional
from flask_babel import lazy_gettext as _l

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[Length(min=3, max=256), Optional()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
