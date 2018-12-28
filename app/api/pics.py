import base64

from flask_restful import Resource, request
from flask import url_for, make_response

from ..models import Pic
from . import api
from .. import db


class PicApi(Resource):
    def get(self, pic_id):
        pic = Pic.query.get(pic_id)
        return make_response(base64.b64decode(pic.base64))

    def put(self, pic_id):
        pass

    def delete(self, pic_id):
        pass


class PicListApi(Resource):
    def get(self):
        return "test"

    def post(self):
        pic = Pic()
        pic.base64 = request.json["base64Code"].split('base64,')[1]
        db.session.add(pic)
        db.session.commit()
        return url_for("api.pic", pic_id=pic.id, _external=True)


api.add_resource(PicApi, '/pics/<int:pic_id>', endpoint='pic')
api.add_resource(PicListApi, '/pics', endpoint='pics')
