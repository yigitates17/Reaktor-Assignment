from . import db


class Games(db.Model):
    game_id = db.Column(db.Integer, primary_key=True, unique=True)
    game_name = db.Column(db.String, unique=True)
    player_A_name = db.Column(db.String())
    player_A_hand = db.Column(db.String())
    player_B_name = db.Column(db.String())
    player_B_hand = db.Column(db.String())


class Players(db.Model):
    player_id = db.Column(db.Integer, primary_key=True, unique=True)
    player_name = db.Column(db.String(), unique=True)
    win = db.Column(db.Integer())
    draw = db.Column(db.Integer())
    lose = db.Column(db.Integer())
    rock = db.Column(db.Integer())
    paper = db.Column(db.Integer())
    scissors = db.Column(db.Integer())


