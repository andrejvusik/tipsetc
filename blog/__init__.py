from flask import Flask, request, current_app
from blog.config.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch


#creating an extensions instances without arguments
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'user.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
moment = Moment()
babel = Babel()


#create an instance of the Flask application
def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from blog.main import bp as main_bp
    app.register_blueprint(main_bp)

    from blog.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from blog.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from blog.post import bp as post_bp
    app.register_blueprint(post_bp, url_prefix='/post')

    from blog.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from blog.translate import bp as translate_bp
    app.register_blueprint(translate_bp, url_prefix='/translate')

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])



from blog import models
