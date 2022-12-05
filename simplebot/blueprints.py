import json
import datetime

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from sqlalchemy import func

from simplebot.database import db
from simplebot.analytics import BotFeedback, BotQuestions
from simplebot.user import User

stats_page = Blueprint("stats_page", __name__, template_folder="templates")


def date_handler(obj): return (
    obj.isoformat()
    if isinstance(obj, (datetime.datetime, datetime.date))
    else obj
)


@stats_page.route("/")
def show():

    # users = db.session.execute(
    #     db.select(User.joined_date, User.last_action_date))
    # users_joined = User.query(func.count())group_by(User.joined_date)
    # users_active = User.query.count().group_by(User.last_action_date)
    # questions = BotQuestions.query.count().group_by(BotQuestions.date_time)
    # feedback = BotFeedback.query.count().group_by(BotFeedback.date_time)

    # users_joined = db.session.query(
    #     User.joined_date, func.count(1)).group_by(User.joined_date)
    # users_active = db.session.query(
    #     User.last_action_date, func.count(1)).group_by(User.joined_date)
    # questions = db.session.query(
    #     BotQuestions.date_time, func.count(1)).group_by(BotQuestions.date_time)
    # feedback = db.session.query(
    #     BotFeedback.date_time, func.count(1)).group_by(BotFeedback.date_time)

    users_joined = db.session.execute(
        db.select(User.joined_date, func.count(1)).group_by(User.joined_date))
    users_active = db.session.execute(
        db.select(User.last_action_date, func.count(1)).group_by(User.joined_date))
    questions = db.session.execute(
        db.select(BotQuestions.date_time, func.count(1)).group_by(BotQuestions.date_time))
    feedback = db.session.execute(
        db.select(BotFeedback.date_time, func.count(1)).group_by(BotFeedback.date_time))

    # for elem in [users_joined, users_active, questions, feedback]:
    #     print(type(elem), elem, sep="\n", end="\n\n")
    #     for elem2 in elem:
    #         print(type(elem2), elem2)
    
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
