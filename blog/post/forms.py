from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, Optional
from flask_babel import lazy_gettext as _l
from blog.models import Categorys


class CreateEditPostForm(FlaskForm):
    title = StringField(_l('Posts title:'), validators=[DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Post URL (optional):'), validators=[Length(min=0, max=128), Optional()])
    content = TextAreaField(_l('Content post:'), validators=[DataRequired(), InputRequired()])
    category = SelectField(_l('Category:'), choices=[])
    submit = SubmitField(_l('Save post'))

    def set_choices(self):
        self.category.choices = [(i.name) for i in Categorys.query.all()]



class CreateEditPostFormAdmin(FlaskForm):
    userid = StringField(_l('User ID'), validators=[DataRequired(), InputRequired()])
    title = StringField(_l('Posts title:'), validators=[DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Post URL (optional):'), validators=[Length(min=0, max=128), Optional()])
    content = TextAreaField(_l('Content post:'), validators=[DataRequired(), InputRequired()])
    category = SelectField(_l('Category:'), choices=[])
    published = BooleanField(_l('Publish after saving'))
    submit = SubmitField(_l('Save post'))

    def set_choices(self):
        self.category.choices = [(i.name) for i in Categorys.query.all()]
