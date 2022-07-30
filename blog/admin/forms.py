from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, InputRequired, Length, Optional
from flask_babel import lazy_gettext as _l
from blog.models import Categorys, Tags


class CreateCategoryForm(FlaskForm):
    name = StringField(_l('Category name:'), validators=[DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Category URL (optional):'), validators=[Length(min=0, max=128), Optional()])
    submit = SubmitField(_l('Save category'))

    def validate_name(self, name):
        category = Categorys.query.filter_by(name=name.data).first()
        if category is not None:
            raise ValidationError(_l('A category with the same name has already been created.'))


class EditCategoryForm(FlaskForm):
    name = StringField(_l('Category name:'), validators=[DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Category URL (optional):'), validators=[Length(min=0, max=128), Optional()])
    submit = SubmitField(_l('Save category'))


class CreateTagForm(FlaskForm):
    name = StringField(_l('Tag name:'), validators=[DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Tag URL (optional):'), validators=[Length(min=0, max=128), Optional()])
    submit = SubmitField(_l('Save tag'))

    def validate_name(self, name):
        tag = Tags.query.filter_by(name=name.data).first()
        if tag is not None:
            raise ValidationError(_l('The same tag has already been created.'))


class EditTagForm(FlaskForm):
    name = StringField(_l('Tag name:'), validators=[DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Tag URL (optional):'), validators=[Length(min=0, max=128), Optional()])
    submit = SubmitField(_l('Save tag'))
