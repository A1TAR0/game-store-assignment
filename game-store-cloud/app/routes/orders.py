from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app.models.order import Order
from app.models.game import Game
import requests

bp = Blueprint('orders', __name__, url_prefix='/orders')

def get_cart():
    """Get cart from session"""
    return session.get('cart', {})

def save_cart(cart):
    """Save cart to session"""
    session['cart'] = cart
    session.modified = True

@bp.route('/cart')
def cart():
    """Display shopping cart"""
    cart = get_cart()
    cart_items = []
    total = 0
    
    for game_id, quantity in cart.items():
        game = Game.find_by_id(game_id)
        if game:
            item_total = game.price * quantity
            cart_items.append({
                'game': game,
                'quantity': quantity,
                'item_total': item_total
            })
            total += item_total
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@bp.route('/add/<game_id>', methods=['POST'])
def add_to_cart(game_id):
    """Add item to cart"""
    if 'user_id' not in session:
        flash('Please log in to add items to cart', 'error')
        return redirect(url_for('auth.login'))
    
    quantity = int(request.form.get('quantity', 1))
    
    # Verify game exists and has stock
    game = Game.find_by_id(game_id)
    if not game:
        flash('Game not found', 'error')
        return redirect(url_for('games.list_games'))
    
    if game.stock_quantity < quantity:
        flash('Not enough stock available', 'error')
        return redirect(url_for('games.game_detail', game_id=game_id))
    
    # Add to cart
    cart = get_cart()
    if game_id in cart:
        cart[game_id] += quantity
    else:
        cart[game_id] = quantity
    
    save_cart(cart)
    flash(f'Added {game.title} to cart!', 'success')
    return redirect(url_for('orders.cart'))

@bp.route('/update/<game_id>', methods=['POST'])
def update_cart(game_id):
    """Update item quantity in cart"""
    quantity = int(request.form.get('quantity', 0))
    
    cart = get_cart()
    if quantity > 0:
        cart[game_id] = quantity
    else:
        cart.pop(game_id, None)
    
    save_cart(cart)
    flash('Cart updated', 'success')
    return redirect(url_for('orders.cart'))

@bp.route('/remove/<game_id>')
def remove_from_cart(game_id):
    """Remove item from cart"""
    cart = get_cart()
    cart.pop(game_id, None)
    save_cart(cart)
    flash('Item removed from cart', 'success')
    return redirect(url_for('orders.cart'))

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Process checkout"""
    if 'user_id' not in session:
        flash('Please log in to checkout', 'error')
        return redirect(url_for('auth.login'))
    
    cart = get_cart()
    if not cart:
        flash('Your cart is empty', 'error')
        return redirect(url_for('games.list_games'))
    
    if request.method == 'POST':
        # Prepare order items
        cart_items = []
        total = 0
        email_items = []
        
        for game_id, quantity in cart.items():
            game = Game.find_by_id(game_id)
            if game:
                cart_items.append({
                    'game_id': game_id,
                    'price': game.price,
                    'quantity': quantity
                })
                total += game.price * quantity
                email_items.append({
                    'title': game.title,
                    'quantity': quantity
                })
        
        try:
            # Create order
            order_id = Order.create(session['user_id'], total, cart_items)
            
            # Get user email from database
            from app.models.user import User
            conn = get_sql_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE user_id = %s", (session['user_id'],))
            user_email = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            
            # Call Cloud Function to send email (if running)
            try:
                email_data = {
                    'email': user_email,
                    'order_id': order_id,
                    'total': total,
                    'items': email_items
                }
                # Note: Update this URL when you deploy the function
                # For local testing: http://localhost:8080
                # requests.post('CLOUD_FUNCTION_URL', json=email_data)
                print(f"Would send email to {user_email} for order {order_id}")
            except Exception as e:
                print(f"Email notification failed: {e}")
                # Don't fail the order if email fails
            
            # Clear cart
            session.pop('cart', None)
            
            flash(f'Order #{order_id} placed successfully!', 'success')
            return redirect(url_for('orders.order_confirmation', order_id=order_id))
        except Exception as e:
            flash(f'Error processing order: {str(e)}', 'error')
            return redirect(url_for('orders.cart'))
    
    # GET request - show checkout page
    cart_items = []
    total = 0
    
    for game_id, quantity in cart.items():
        game = Game.find_by_id(game_id)
        if game:
            item_total = game.price * quantity
            cart_items.append({
                'game': game,
                'quantity': quantity,
                'item_total': item_total
            })
            total += item_total
    
    return render_template('checkout.html', cart_items=cart_items, total=total)

@bp.route('/confirmation/<int:order_id>')
def order_confirmation(order_id):
    """Show order confirmation"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get order details
    orders = Order.get_user_orders(session['user_id'])
    order = next((o for o in orders if o.order_id == order_id), None)
    
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('orders.my_orders'))
    
    # Get order items
    items = Order.get_order_items(order_id)
    order_items = []
    
    for item in items:
        game = Game.find_by_id(item['game_id'])
        if game:
            order_items.append({
                'game': game,
                'quantity': item['quantity'],
                'price': item['price']
            })
    
    return render_template('order_confirmation.html', order=order, items=order_items)

@bp.route('/')
def my_orders():
    """Display user's orders"""
    if 'user_id' not in session:
        flash('Please log in to view orders', 'error')
        return redirect(url_for('auth.login'))
    
    orders = Order.get_user_orders(session['user_id'])
    
    # Get items for each order
    for order in orders:
        order.items = Order.get_order_items(order.order_id)
        # Get game details for each item
        for item in order.items:
            game = Game.find_by_id(item['game_id'])
            item['game'] = game
    
    return render_template('orders.html', orders=orders)

@bp.route('/api/cart', methods=['GET'])
def api_get_cart():
    """REST API to get cart contents"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    cart = get_cart()
    return jsonify({'cart': cart, 'item_count': sum(cart.values())})