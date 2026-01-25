from flask import Flask, render_template
from app.routes import auth, games, orders, admin, wishlist
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, 
            template_folder='app/templates',
            static_folder='app/static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(games.bp)
app.register_blueprint(orders.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(wishlist.bp) 

@app.route('/')
def index():
    return render_template('index.html')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)