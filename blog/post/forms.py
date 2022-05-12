from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, Optional
from flask_babel import lazy_gettext as _l


class CreateEditPostForm(FlaskForm):
    title = StringField(_l('Posts title:'), validators=[
                        DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Post URL (optional):'), validators=[
                       Length(min=0, max=128), Optional()])
    content = TextAreaField(_l('Content post:'), validators=[
                            DataRequired(), InputRequired()])
    category = StringField(_l('Category:'), validators=[
                           DataRequired(), InputRequired(), Length(min=0, max=64)])
    submit = SubmitField(_l('Save post'))


class CreateEditPostFormAdmin(FlaskForm):
    userid = StringField(_l('User ID'), validators=[
                         DataRequired(), InputRequired()])
    title = StringField(_l('Posts title:'), validators=[
                        DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Post URL (optional):'), validators=[
                       Length(min=0, max=128), Optional()])
    content = TextAreaField(_l('Content post:'), validators=[
                            DataRequired(), InputRequired()])
    category = StringField(_l('Category:'), validators=[
                           DataRequired(), InputRequired(), Length(min=0, max=64)])
    published = BooleanField(_l('Publish after saving'))
    submit = SubmitField(_l('Save post'))
