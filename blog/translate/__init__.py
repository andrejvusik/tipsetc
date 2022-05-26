from flask import Blueprint

bp = Blueprint('translate', __name__)

from blog.translate import view
