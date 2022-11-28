import json
import datetime

from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from simplebot.database import db
from simplebot.user import User

stats_page = Blueprint("stats_page", __name__, template_folder="templates")


def date_handler(obj): return (
    obj.isoformat()
    if isinstance(obj, (datetime.datetime, datetime.date))
    else obj
)


@stats_page.route("/")
def show():

    # users = db.session.query(User)
    users = db.session.execute(
        db.select(User.joined_date, User.last_action_date))
    # users = db.session.query(User.id)

    data = list()
    for user in users:
        data.append([user.joined_date, user.last_action_date])

    users = json.dumps(data, default=date_handler)
    try:
        return render_template(f"statistics.html", users=users)
    except TemplateNotFound:
        abort(404)
