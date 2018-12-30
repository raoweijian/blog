import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
from flask_login import UserMixin

from . import db
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Article(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    __mapper_args__ = {
        "order_by": create_time.desc()
    }


    def __repr__(self):
        return '<Article %r>' % self.title

    def to_json(self):
        ret = {
            'id': self.id,
            "title": self.title,
            "link": url_for("main.article", article_id=self.id),
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "modify_time": self.modify_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return ret

    def to_full_json(self):
        ret = {
            'id': self.id,
            "title": self.title,
            "content": self.content,
            "link": url_for("main.article", article_id=self.id),
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "modify_time": self.modify_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return ret

    def set_by_json(self, json_data):
        self.title = json_data["title"]
        self.content = json_data["content"]


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Pic(db.Model):
    __tablename__ = "pics"
    id = db.Column(db.Integer, primary_key=True)
    base64 = db.Column(db.Text, nullable=False)
