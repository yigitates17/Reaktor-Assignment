from flask import Blueprint, render_template
from .functions import game_data, home_games, update_player, player_profile

views = Blueprint('views', __name__)


@views.route('/')
def home():
    game_data()
    return render_template('home.html', matches=home_games()[0], players=home_games()[1])


@views.route('/profile/<string:profile_id>')
def profile(profile_id):
    update_player(profile_id)
    return render_template('profile.html', player_data=player_profile(profile_id))
