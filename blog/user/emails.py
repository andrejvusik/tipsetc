from blog import current_app, mail
from blog.models import Users
from flask import render_template
from flask_mail import Message
from flask_babel import _
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(_('[TipsEtc...] Reset your password.'),
               sender=current_app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template(
                   'emails/reset_password.txt', user=user, token=token),
               html_body=render_template('emails/reset_password.html', user=user, token=token))


def send_reg_new_user(user):
    send_email(_('[TipsEtc...] New user registered.'),
               sender=current_app.config['MAIL_USERNAME'],
               recipients=current_app.config['ADMINS'],
               text_body=render_template('emails/reg_new_user.txt', user=user),
               html_body=render_template('emails/reg_new_user.html', user=user))


def send_confirm_email(user):
    token = user.generate_confirmation_token()
    send_email(_('[TipsEtc...] Confirmation of registration.'),
               sender=current_app.config['MAIL_USERNAME'],
               recipients=[user.email],
               text_body=render_template(
                   'emails/confirm_email.txt', user=user, token=token),
               html_body=render_template('emails/confirm_email.html', user=user, token=token))
