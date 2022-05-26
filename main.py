from flask import current_app
from blog import create_app
from blog.config.config import Config


app = create_app(Config)
