from blog.translate import bp
from flask import request, jsonify
from blog.translate.translate import translate
from flask_login import login_required


@bp.route('/title', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['source_language'], request.form['dest_language'], request.form['text'])})
