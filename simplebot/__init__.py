from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from config import DEVELOPMENT, SECRET_KEY



db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def init_app():
    import nltk
    nltk.download('punkt')
    
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bot.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)
    # db.create_all()
    migrate.init_app(app, db)
    login.init_app(app)
    
    from simplebot.admin import Admin
    from .blueprints import stats_page, index_page, register_page, login_page, logout_page

    login.login_view = "login_page.login"

    @login.user_loader
    def load_admin(id):
        return Admin.query.get(int(id))
    

    app.register_blueprint(stats_page, url_prefix="/stats")
    app.register_blueprint(index_page, url_prefix="/index")
    app.register_blueprint(register_page, url_prefix="/register")
    app.register_blueprint(login_page, url_prefix="/login")
    app.register_blueprint(logout_page, url_prefix="/logout")
    
    return app
