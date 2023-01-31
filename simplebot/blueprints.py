import json
import datetime

from flask import Blueprint, render_template, abort, redirect, url_for, flash, request, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from jinja2 import TemplateNotFound
from sqlalchemy import func

from simplebot.database import db
from simplebot.analytics import BotFeedback, BotQuestions
from simplebot.user import User
from simplebot.admin import Admin
from simplebot.forms import LoginForm, RegistrationForm

index_page = Blueprint("index_page", __name__, template_folder="templates")
stats_page = Blueprint("stats_page", __name__, template_folder="templates")
register_page = Blueprint("register_page", __name__, template_folder="templates")
login_page = Blueprint("login_page", __name__, template_folder="templates")
logout_page = Blueprint("logout_page", __name__, template_folder="templates")

def date_handler(obj): return (
    obj.isoformat()
    if isinstance(obj, (datetime.datetime, datetime.date))
    else obj
)


# @login_required
@stats_page.route("/")
def stats():
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()
    users_joined = db.session.execute(
        db.select(func.strftime("%Y-%m-%d", User.joined_date), func.count(1))
            .group_by(func.strftime("%Y-%m-%d", User.joined_date)))
    users_active = db.session.execute(
        db.select(func.strftime("%Y-%m-%d", User.last_action_date), func.count(1))
            .group_by(func.strftime("%Y-%m-%d", User.last_action_date)))
    questions = db.session.execute(
        db.select(func.strftime("%Y-%m-%d", BotQuestions.date_time), func.count(1))
            .group_by(func.strftime("%Y-%m-%d", BotQuestions.date_time)))
    feedback = db.session.execute(
        db.select(func.strftime("%Y-%m-%d", BotFeedback.date_time), func.count(1))
            .group_by(func.strftime("%Y-%m-%d", BotFeedback.date_time)))

    users_joined = [{"date": elem[0], "count": elem[1]} for elem in users_joined]
    users_active = [{"date": elem[0], "count": elem[1]} for elem in users_active]
    questions = [{"date": elem[0], "count": elem[1]} for elem in questions]
    feedback = [{"date": elem[0], "count": elem[1]} for elem in feedback]
    
    users_joined = json.dumps(users_joined, default=date_handler)
    users_active = json.dumps(users_active, default=date_handler)
    questions = json.dumps(questions, default=date_handler)
    feedback = json.dumps(feedback, default=date_handler)

    try:
        return render_template(f"statistics.html", users_joined=users_joined, users_active=users_active,
                               questions=questions, feedback=feedback)
    except TemplateNotFound:
        abort(404)


@index_page.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Home Page")

@register_page.route("/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index_page.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Admin(username=form.username.data, email=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You are now registered.")
        return redirect(url_for("login_page.login"))
    return render_template("register.html", title="Register", form=form)
    
@login_page.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index_page.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login_page.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index_page.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)
            

@logout_page.route("/", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("index_page.index"))