from datetime import datetime

from simplebot import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viber_id = db.Column(db.Integer, unique=True)
    login = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    name = db.Column(db.String(50))
    google_login = db.Column(db.String(50))
    google_password = db.Column(db.String(50))
    linkedin_login = db.Column(db.String(50))
    linkedin_password = db.Column(db.String(50))
    discord_login = db.Column(db.String(50))
    step_index = db.Column(db.Integer)
    dialog_status = db.Column(db.String(10), default="message")
    keyboard = db.Column(db.Text())
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_action_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"id:{self.id}, step_index:{self.step_index}, dialog_status:{self.dialog_status}"


class UserDatabase:
    def create_user(self, viber_id):
        user = User(viber_id=viber_id)
        db.session.add(user)
        db.session.commit()
        return user

    def get_user(self, viber_id):
        # user = User.query.filter_by(viber_id=viber_id).first()
        user = db.session.query(User).filter_by(viber_id=viber_id).first()
        if user is None:
            user = self.create_user(viber_id)
        return user

    def update_user(self):
        db.session.commit()
    
    def delete_user(self, viber_id):
        db.session.query(User).filter_by(viber_id=viber_id).delete()
        db.session.commit()
