from flask import Blueprint, render_template, session, redirect, url_for, flash

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/')
def my_orders():
    """Display user's orders"""
    if 'user_id' not in session:
        flash('Please log in to view orders', 'error')
        return redirect(url_for('auth.login'))
    
    # TODO: Implement order retrieval
    return render_template('orders.html')

@bp.route('/cart')
def cart():
    """Display shopping cart"""
    # TODO: Implement cart functionality
    return render_template('cart.html')