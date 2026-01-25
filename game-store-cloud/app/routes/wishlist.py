from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify
from app.models.wishlist import Wishlist
from app.models.game import Game

bp = Blueprint('wishlist', __name__, url_prefix='/wishlist')

@bp.route('/')
def view_wishlist():
    """Display user's wishlist"""
    if 'user_id' not in session:
        flash('Please log in to view your wishlist', 'error')
        return redirect(url_for('auth.login'))
    
    game_ids = Wishlist.get_user_wishlist(session['user_id'])
    
    # Get game details
    games = []
    for game_id in game_ids:
        game = Game.find_by_id(game_id)
        if game:
            games.append(game)
    
    return render_template('wishlist.html', games=games)

@bp.route('/add/<game_id>', methods=['POST'])
def add_to_wishlist(game_id):
    """Add game to wishlist"""
    if 'user_id' not in session:
        flash('Please log in to add to wishlist', 'error')
        return redirect(url_for('auth.login'))
    
    game = Game.find_by_id(game_id)
    if not game:
        flash('Game not found', 'error')
        return redirect(url_for('games.list_games'))
    
    added = Wishlist.add_game(session['user_id'], game_id)
    
    if added:
        flash(f'{game.title} added to wishlist!', 'success')
    else:
        flash(f'{game.title} is already in your wishlist', 'info')
    
    return redirect(url_for('games.game_detail', game_id=game_id))

@bp.route('/remove/<game_id>')
def remove_from_wishlist(game_id):
    """Remove game from wishlist"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    Wishlist.remove_game(session['user_id'], game_id)
    flash('Game removed from wishlist', 'success')
    return redirect(url_for('wishlist.view_wishlist'))

@bp.route('/api/check/<game_id>')
def check_wishlist(game_id):
    """API endpoint to check if game is in wishlist"""
    if 'user_id' not in session:
        return jsonify({'in_wishlist': False})
    
    in_wishlist = Wishlist.is_in_wishlist(session['user_id'], game_id)
    return jsonify({'in_wishlist': in_wishlist})