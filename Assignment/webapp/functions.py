import requests
from .models import Games, Players
from . import db

# WILL BE FIXED AFTER LEARNING ASYNC PROGRAMMING
"""def game_data():
    website = "https://bad-api-assignment.reaktor.com"
    next_page = "/rps/history"
    while True:
        url = website + next_page
        page = requests.get(url=url)
        page = page.json()
        if page["cursor"]:
            next_page = page["cursor"]
            if page["data"]:
                for data in page["data"]:
                    game = Games(game_name=data.gameId, player_A_name=data.playerA.name,
                                 player_A_hand=data.playerA.played, player_B_name=data.playerB.name,
                                 player_B_hand=data.playerB.played)
                    db.session.add(game)
            else:
                db.session.commit()
                break
        else:
            db.session.commit()
            break"""


def game_data():
    website = "https://bad-api-assignment.reaktor.com"
    next_page = "/rps/history"
    for _ in range(0, 2):
        url = website + next_page
        page = requests.get(url=url)
        page = page.json()
        next_page = page["cursor"]
        for data in page["data"]:
            game = Games(game_name=data["gameId"], player_A_name=data["playerA"]["name"],
                         player_A_hand=data["playerA"]["played"], player_B_name=data["playerB"]["name"],
                         player_B_hand=data["playerB"]["played"])

            playerA = Players(player_name=data["playerA"]["name"])
            playerB = Players(player_name=data["playerB"]["name"])

            game_exists = db.session.query(Games).filter_by(game_name=data["gameId"]).first() is not None
            playerA_exists = db.session.query(Players).filter_by(
                player_name=data["playerA"]["name"]).first() is not None
            playerB_exists = db.session.query(Players).filter_by(
                player_name=data["playerB"]["name"]).first() is not None

            if not game_exists:
                db.session.add(game)

            if not playerA_exists:
                db.session.add(playerA)

            if not playerB_exists:
                db.session.add(playerB)

    db.session.commit()


def home_games():
    games = db.session.query(Games).order_by(Games.game_id.desc()).limit(50)
    games = games[::-1]
    games_data = list()
    player_dicts = dict()
    for game in games:
        player = db.session.query(Players).filter_by(player_name=game.player_A_name).first()
        player_dict = {game.player_A_name: player.player_id}
        player_dicts.update(player_dict)
    games_data.append(games)
    games_data.append(player_dicts)
    return games_data


def update_player(profile_id):
    table = {'ROCK': {"ROCK": "draw", "PAPER": "lose", "SCISSORS": "win"},  # r-p-s table for each case
             'PAPER': {"PAPER": "draw", "SCISSORS": "lose", "ROCK": "win"},  # without if statements
             'SCISSORS': {"SCISSORS": "draw", "ROCK": "lose", "PAPER": "win"}}

    player = db.session.query(Players).filter_by(player_id=profile_id).first()

    playerA = db.session.query(Games).filter_by(player_A_name=player.player_name).all()
    playerB = db.session.query(Games).filter_by(player_B_name=player.player_name).all()

    rock_A = len(db.session.query(Games).filter_by(player_A_name=player.player_name, player_A_hand="ROCK").all())
    paper_A = len(db.session.query(Games).filter_by(player_A_name=player.player_name, player_A_hand="PAPER").all())
    scissors_A = len(
        db.session.query(Games).filter_by(player_A_name=player.player_name, player_A_hand="SCISSORS").all())

    rock_B = len(db.session.query(Games).filter_by(player_B_name=player.player_name, player_B_hand="ROCK").all())
    paper_B = len(db.session.query(Games).filter_by(player_B_name=player.player_name, player_B_hand="PAPER").all())
    scissors_B = len(
        db.session.query(Games).filter_by(player_B_name=player.player_name, player_B_hand="SCISSORS").all())

    hands = {"rock": rock_A + rock_B, "paper": paper_A + paper_B, "scissors": scissors_A + scissors_B}

    match_history_status_A = [table[row.player_A_hand][row.player_B_hand] for row in playerA]
    match_history_status_B = [table[row.player_B_hand][row.player_A_hand] for row in playerB]
    match_history_status = match_history_status_A + match_history_status_B

    win = match_history_status.count("win")
    lose = match_history_status.count("lose")
    draw = match_history_status.count("draw")

    player.win = win
    player.lose = lose
    player.draw = draw
    player.rock = hands["rock"]
    player.paper = hands["paper"]
    player.scissors = hands["scissors"]

    db.session.commit()


def player_profile(profile_id):
    player = db.session.query(Players).filter_by(player_id=profile_id).first()
    playerA = db.session.query(Games).filter_by(player_A_name=player.player_name).all()
    playerB = db.session.query(Games).filter_by(player_B_name=player.player_name).all()

    player_name = player.player_name
    total_games = len(
        Games.query.filter((Games.player_A_name == player_name) | (Games.player_B_name == player_name)).all())

    hands = {player.rock: "rock", player.paper: "paper", player.scissors: "scissors"}
    most_played_hand = hands[max(hands)]
    match_history = Games.query.filter(
        (Games.player_A_name == player_name) | (Games.player_B_name == player_name)).order_by(
        Games.game_id.desc()).limit(20)
    match_history = match_history[::-1]

    player_dicts = dict()
    for match in match_history:
        playerA = db.session.query(Players).filter_by(player_name=match.player_A_name).first()
        player_dict = {match.player_A_name: playerA.player_id}
        player_dicts.update(player_dict)
        playerB = db.session.query(Players).filter_by(player_name=match.player_B_name).first()
        player_dict = {match.player_B_name: playerB.player_id}
        player_dicts.update(player_dict)

    win_rate = round(100 * player.win / total_games)

    player_data = {"player_name": player_name, "total_games": total_games, "most_played_hand": most_played_hand,
                   "win_rate": win_rate, "player_row": player, "match_history": match_history,
                   "players_id": player_dicts}

    return player_data
