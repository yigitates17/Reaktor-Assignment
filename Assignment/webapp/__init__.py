from os import path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"


def create_database(app):
    if not path.exists('webapp/' + DB_NAME):
        db.create_all(app=app)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Reaktor123"
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////PyCharm Projects/Assignment/webapp/database.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.jinja_env.filters['game_result'] = game_result

    from .models import Games, Players

    create_database(app)

    return app


def game_result(playerA, playerB):
    table = {'ROCK': {"ROCK": "gray", "PAPER": "#FF1744", "SCISSORS": "#00C853"},
             'PAPER': {"PAPER": "gray", "SCISSORS": "#FF1744", "ROCK": "#00C853"},
             'SCISSORS': {"SCISSORS": "gray", "ROCK": "#FF1744", "PAPER": "#00C853"}}

    playerA_status = table[playerA][playerB]

    return playerA_status
