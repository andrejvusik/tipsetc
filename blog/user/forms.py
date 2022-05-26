from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, Length, Optional
from blog.models import Users
from flask_login import current_user
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remain in the system'))
    submit = SubmitField(_l('Sign in'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Restore password'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired(), InputRequired()])
    password2 = PasswordField(_l('Confirm password'), validators=[DataRequired(), InputRequired(), EqualTo('password')])
    submit = SubmitField(_l('Save new password'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired(), InputRequired()])
    full_name = StringField(_l('Full name (optional)'), validators=[Length(min=0, max=128)])
    email = StringField(_l('Email'), validators=[DataRequired(), InputRequired(), Email()])
    telegram = StringField(_l('Username Telegram (optional)'), validators=[Length(min=0, max=128), Optional()])
    show_personal = BooleanField(_l('Show personal details (Email, Telegram)'))
    password = PasswordField(_l('Password'), validators=[DataRequired(), InputRequired()])
    password2 = PasswordField(_l('Confirm password'), validators=[DataRequired(), InputRequired(), EqualTo('password')])
    about_me = TextAreaField(_l('About me (optional)'), validators=[Length(min=0, max=256), Optional()])
    agree_terms = BooleanField(_l('I accept the terms of the user agreement'))
    submit = SubmitField(_l('Registration'))

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different username.'))

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('Please use a different email address.'))


class EditProfilForm(FlaskForm):
    userid = StringField(_l('ID user'), validators=[DataRequired(), InputRequired()])
    username = StringField(_l('Username'), validators=[DataRequired(), InputRequired()])
    full_name = StringField(_l('Full name (optional)'), validators=[Length(min=0, max=128), Optional()])
    email = StringField(_l('Email'), validators=[DataRequired(), InputRequired(), Email()])
    telegram = StringField(_l('Username Telegram (optional)'), validators=[Length(min=0, max=128), Optional()])
    show_personal = BooleanField(_l('Show personal details (Email, Telegram)'))
    about_me = TextAreaField(_l('About me (optional)'), validators=[Length(min=0, max=256), Optional()])
    admin = BooleanField(_l('Admin'))
    author = BooleanField(_l('Author'))
    confirmed = BooleanField(_l('Account verified'))
    submit = SubmitField(_l('Update Profile'))

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user is not None:
            if user.username is not user.username:
                raise ValidationError(_l('Please use a different username.'))

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            if user.email is not user.email:
                raise ValidationError(
                    _l('Please use a different email address.'))
