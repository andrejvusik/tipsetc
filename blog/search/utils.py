from flask import g, render_template, redirect, url_for, request, current_app,flash
from flask_babel import _
from blog.models import Posts
from werkzeug.urls import url_parse


class BlogSearch(object):

    def __init__(self, *args, **kwargs):
        super(BlogSearch, self).__init__(*args, **kwargs)

    def search_blog(title):
        page = request.args.get('page', 1, type=int)
        posts = Posts.query.filter_by(published="1").whooshee_search(g.search_form.q.data, order_by_relevance=2).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
        paginationlist = {
        'first_url': url_for('search.search', q=g.search_form.q.data, page=1),
        'prev_url': url_for('search.search', q=g.search_form.q.data, page=posts.prev_num),
        'this_url': url_for('search.search', q=g.search_form.q.data, page=posts.page),
        'next_url': url_for('search.search', q=g.search_form.q.data, page=posts.next_num),
        'last_url': url_for('search.search', q=g.search_form.q.data, page=posts.pages),
        'first_lable': 1,
        'prev_lable': posts.prev_num,
        'this_lable': posts.page,
        'next_lable': posts.next_num,
        'last_lable': posts.pages
        }
        if Posts.query.filter_by(published="1").whooshee_search(g.search_form.q.data, order_by_relevance=2).count() == 0:
            back_page = request.referrer
            if not back_page or back_page != request.referrer:
                back_page = url_for('main.index')
            flash(_('No results were found for "%(searchrequest)s". Try other keywords.', searchrequest=g.search_form.q.data))
            return redirect(back_page)
        else:
            return render_template('post/index.html', title=title, posts=posts.items, paginationlist=paginationlist)
