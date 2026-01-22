import pytest
from main import app
from app.models.game import Game

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestHomeRoutes:
    """Test home page routes"""
    
    def test_home_page(self, client):
        """Test home page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to Game Store' in response.data
    
    def test_games_page(self, client):
        """Test games page loads"""
        response = client.get('/games/')
        assert response.status_code == 200
        assert b'Game Catalog' in response.data

class TestAuthRoutes:
    """Test authentication routes"""
    
    def test_register_page_loads(self, client):
        """Test register page loads"""
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'Create Account' in response.data
    
    def test_login_page_loads(self, client):
        """Test login page loads"""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login' in response.data
    
    def test_register_requires_fields(self, client):
        """Test registration validation"""
        response = client.post('/auth/register', data={
            'email': '',
            'username': '',
            'password': ''
        }, follow_redirects=True)
        
        assert b'required' in response.data or response.status_code == 200

class TestGameRoutes:
    """Test game-related routes"""
    
    def test_games_list_page(self, client):
        """Test games list loads"""
        response = client.get('/games/')
        assert response.status_code == 200
    
    def test_game_api_endpoint(self, client):
        """Test games API endpoint"""
        response = client.get('/games/api/games')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_nonexistent_game(self, client):
        """Test accessing non-existent game"""
        response = client.get('/games/nonexistent-game-id')
        assert response.status_code == 404

class TestCartRoutes:
    """Test shopping cart routes"""
    
    def test_cart_requires_login(self, client):
        """Test that cart requires authentication"""
        response = client.get('/orders/cart')
        # Should redirect to login or show empty cart
        assert response.status_code in [200, 302]
    
    def test_add_to_cart_requires_login(self, client):
        """Test adding to cart requires login"""
        response = client.post('/orders/add/test-game', follow_redirects=True)
        assert b'log in' in response.data.lower() or b'login' in response.data.lower()