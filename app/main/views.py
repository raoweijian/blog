import json
import time

from flask import render_template, request, Response, abort
from flask_login import login_required
import requests

from . import main
from .. import db
from ..models import Article

@main.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@main.route('/article/<int:article_id>', methods=['GET'])
def article(article_id):
    if Article.query.get(article_id) is None:
        abort(404)
    return render_template("article.html")


@main.route('/article/<int:article_id>/edit', methods=['GET'])
@login_required
def edit(article_id):
    return render_template("edit.html")


@main.route('/article/new', methods=['GET'])
@login_required
def new():
    return render_template("edit.html")
