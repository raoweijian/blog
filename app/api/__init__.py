from flask import Blueprint
from ..models import *

from flask_restful import Resource, Api

bp = Blueprint('api', __name__)
api = Api(bp)

from . import articles, pics
