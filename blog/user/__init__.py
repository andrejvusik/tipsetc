from flask import Blueprint

bp = Blueprint('user', __name__)

from blog.user import view
