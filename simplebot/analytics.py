from datetime import datetime

from simplebot.database import db


class BotQuestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    question = db.Column(db.String(150))
    date_time = db.Column(db.DateTime)


class BotFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    feedback = db.Column(db.String(150))
    date_time = db.Column(db.DateTime)


class Analytics:
    def add_question(self, viber_id, question):
        entry = BotQuestions(
            user_id=viber_id, question=question, date_time=datetime.utcnow()
        )
        db.session.add(entry)
        db.session.commit()
        return

    def add_feedback(self, viber_id, feedback):
        entry = BotFeedback(
            user_id=viber_id, feedback=feedback, date_time=datetime.utcnow()
        )
        db.session.add(entry)
        db.session.commit()
        return
