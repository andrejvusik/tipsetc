from flask import Blueprint

bp = Blueprint('admin', __name__)

from blog.admin import view
