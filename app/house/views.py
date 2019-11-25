from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User


@auth.route('/', methods=['GET'])
def login():
    return render_template('house/index.html')
