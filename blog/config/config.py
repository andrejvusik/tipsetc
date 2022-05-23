import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #SECRET KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secretkeyformytipsetc...flask'

    #DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '../../db/blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #PAGINATION
    POSTS_PER_PAGE = 5

    # MAIL
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.yandex.ru'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'elektriks@tut.by'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'ndvvvmurnyhxwfbz'
    ADMINS = ['andrejvusik@gmail.com']

    #BABEL
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    LANGUAGES = ['ru', 'en']

    #TRANSLATE
    TRANSLATE_URL = os.environ.get('TRANSLATE_URL') or 'https://translate.google.com/translate_a/single?client=at&dt=t&dt=ld&dt=qca&dt=rm&dt=bd&dj=1&hl=uk-RU&ie=UTF-8&oe=UTF-8&inputm=2&otf=2&iid=1dd3b944-fa62-4b55-b330-74909a99969e'

    #SEARCH
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
