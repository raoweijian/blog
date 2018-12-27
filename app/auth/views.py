from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.json["username"]).first()
        if user is None or not user.verify_password(request.json["password"]):
            return "用户名或密码错误"
        else:
            login_user(user, request.json["remember"])
            return "ok"

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
