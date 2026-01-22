from flask import Blueprint, render_template, request, jsonify
from app.models.game import Game

bp = Blueprint('games', __name__, url_prefix='/games')

@bp.route('/')
def list_games():
    """Display all games"""
    games = Game.get_all()
    return render_template('games.html', games=games)

@bp.route('/<game_id>')
def game_detail(game_id):
    """Display single game details"""
    game = Game.find_by_id(game_id)
    if game:
        return render_template('game_detail.html', game=game)
    return "Game not found", 404

@bp.route('/api/games', methods=['GET'])
def api_list_games():
    """REST API endpoint to get all games"""
    games = Game.get_all()
    return jsonify([{
        'game_id': g.game_id,
        'title': g.title,
        'price': g.price,
        'genre': g.genre,
        'platform': g.platform
    } for g in games])