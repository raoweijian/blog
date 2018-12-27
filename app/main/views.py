import json
import time

from flask import render_template, request, Response
import requests

from . import main
from .. import db
from ..models import *

@main.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@main.route('/article/<int:article_id>', methods=['GET'])
def article(article_id):
    return render_template("article.html")


@main.route('/article/<int:article_id>/edit', methods=['GET'])
def edit(article_id):
    return render_template("edit.html")


@main.route('/article/new', methods=['GET'])
def new():
    return render_template("edit.html")
