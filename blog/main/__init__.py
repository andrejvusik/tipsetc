from flask import Blueprint

bp = Blueprint('main', __name__)

from blog.main import view
