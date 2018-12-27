from flask_restful import Resource, request
from flask import url_for

from ..models import Article
from . import api
from .. import db


class ArticleApi(Resource):
    def get(self, article_id):
        article = Article.query.get(article_id)
        return article.to_full_json()

    def put(self, article_id):
        article = Article.query.get(article_id)
        article.set_by_json(request.json)
        db.session.add(article)
        db.session.commit()
        return url_for("main.article", article_id=article_id)

    def delete(self, article_id):
        article = Article.query.get(article_id)
        db.session.delete(article)
        db.session.commit()


class ArticleListApi(Resource):
    def get(self):
        articles = Article.query.all()
        for i in range(len(articles)):
            articles[i] = articles[i].to_json()
        return articles

    def post(self):
        article = Article()
        article.set_by_json(request.json)
        db.session.add(article)
        db.session.commit()
        return url_for("main.article", article_id=article.id)


api.add_resource(ArticleApi, '/articles/<int:article_id>', endpoint='article')
api.add_resource(ArticleListApi, '/articles', endpoint='articles')
