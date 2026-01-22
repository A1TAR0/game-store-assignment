from flask import Flask, render_template
from app.routes import auth, games, orders, admin
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

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)