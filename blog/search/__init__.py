from flask import Blueprint

bp = Blueprint('search', __name__)

from blog.search import view
