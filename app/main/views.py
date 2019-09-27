from flask import render_template, abort
from flask_login import login_required

from . import main
from ..models import Article


@main.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@main.route('/article/<int:article_id>', methods=['GET'])
def article(article_id):
    if Article.query.get(article_id) is None:
        abort(404)
    return render_template("article.html")


@main.route('/moon', methods=['GET'])
def moon():
    return render_template("moon.html")


@main.route('/article/<int:article_id>/edit', methods=['GET'])
@login_required
def edit(article_id):
    return render_template("edit.html")


@main.route('/article/new', methods=['GET'])
@login_required
def new():
    return render_template("edit.html")
