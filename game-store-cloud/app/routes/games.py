from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from app.models.game import Game
from app.utils.db_firestore import db
from datetime import datetime

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

@bp.route('/<game_id>/review', methods=['POST'])
def add_review(game_id):
    """Add a review for a game"""
    if 'user_id' not in session:
        flash('Please log in to write a review', 'error')
        return redirect(url_for('auth.login'))
    
    rating = request.form.get('rating')
    review_text = request.form.get('review_text')
    
    if not rating or not review_text:
        flash('Please provide both rating and review text', 'error')
        return redirect(url_for('games.game_detail', game_id=game_id))
    
    # Add review to Firestore
    review_data = {
        'game_id': game_id,
        'user_id': session['user_id'],
        'username': session['username'],
        'rating': int(rating),
        'review_text': review_text,
        'helpful_count': 0,
        'created_at': datetime.now()
    }
    
    db.collection('reviews').add(review_data)
    flash('Review submitted successfully!', 'success')
    return redirect(url_for('games.game_detail', game_id=game_id))

@bp.route('/api/games', methods=['GET'])
def api_list_games():
    """REST API endpoint to get all games"""
    games = Game.get_all()
    return jsonify([{
        'game_id': g.game_id,
        'title': g.title,
        'price': g.price,
        'genre': g.genre,
        'platform': g.platform,
        'rating': g.rating
    } for g in games])

@bp.route('/api/games/<game_id>', methods=['GET'])
def api_game_detail(game_id):
    """REST API endpoint to get single game"""
    game = Game.find_by_id(game_id)
    if game:
        return jsonify({
            'game_id': game.game_id,
            'title': game.title,
            'description': game.description,
            'price': game.price,
            'publisher': game.publisher,
            'genre': game.genre,
            'platform': game.platform,
            'rating': game.rating,
            'stock_quantity': game.stock_quantity
        })
    return jsonify({'error': 'Game not found'}), 404