from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, InputRequired, Length, Optional
from flask_babel import lazy_gettext as _l
from blog.models import Users, Categorys, Tags


class CreateEditPostForm(FlaskForm):
    title = StringField(_l('Posts title:'), validators=[DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Post URL (optional):'), validators=[Length(min=0, max=128), Optional()])
    content = TextAreaField(_l('Content post:'), validators=[DataRequired(), InputRequired()])
    category = SelectField(_l('Category:'), choices=[])
    submit = SubmitField(_l('Save post'))

    def set_choices(self):
        self.category.choices = [(i.name) for i in Categorys.query.all()]



class CreateEditPostFormAdmin(FlaskForm):
    author = SelectField(_l('Author:'), choices=[])
    title = StringField(_l('Posts title:'), validators=[DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Post URL (optional):'), validators=[Length(min=0, max=128), Optional()])
    content = TextAreaField(_l('Content post:'), validators=[DataRequired(), InputRequired()])
    category = SelectField(_l('Category:'), choices=[])
    published = BooleanField(_l('Publish after saving'))
    submit = SubmitField(_l('Save post'))

    def set_choices(self):
        self.author.choices = [(i.username) for i in Users.query.filter_by(author="1").all()]
        self.category.choices = [(i.name) for i in Categorys.query.all()]
