from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, InputRequired, Length, Optional
from flask_babel import lazy_gettext as _l
from blog.models import Categorys


class CreateEditCategoryForm(FlaskForm):
    name = StringField(_l('Category name:'), validators=[DataRequired(), InputRequired(), Length(min=0, max=128)])
    slug = StringField(_l('Category URL (optional):'), validators=[Length(min=0, max=128), Optional()])
    submit = SubmitField(_l('Save category'))

    def validate_name(self, name):
        category = Categorys.query.filter_by(name=name.data).first()
        if category is not None:
            raise ValidationError(_l('A category with the same name has already been created.'))
