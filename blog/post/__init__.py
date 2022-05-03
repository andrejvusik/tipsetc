from flask import Blueprint

bp = Blueprint('post', __name__)

from blog.post import view
