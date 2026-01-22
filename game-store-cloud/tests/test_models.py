import pytest
from app.models.user import User
from app.models.game import Game
from app.utils.security import hash_password, verify_password
import os
from dotenv import load_dotenv

load_dotenv()

class TestUserModel:
    """Test User model functionality"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        password = "test_password_123"
        hashed = hash_password(password)
        
        # Hash should be different from original
        assert hashed != password
        
        # Should verify correctly
        assert verify_password(hashed, password) == True
        
        # Should fail with wrong password
        assert verify_password(hashed, "wrong_password") == False
    
    def test_password_hash_unique(self):
        """Test that same password creates different hashes"""
        password = "same_password"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Different hashes due to salt
        assert hash1 != hash2
        
        # Both should verify
        assert verify_password(hash1, password) == True
        assert verify_password(hash2, password) == True

class TestGameModel:
    """Test Game model functionality"""
    
    def test_game_creation(self):
        """Test creating a game object"""
        game = Game(
            game_id='test-game',
            title='Test Game',
            description='A test game',
            price=29.99,
            publisher='Test Publisher',
            genre=['Action', 'Adventure'],
            platform=['PC', 'Console'],
            rating=4.5,
            stock_quantity=100
        )
        
        assert game.game_id == 'test-game'
        assert game.title == 'Test Game'
        assert game.price == 29.99
        assert 'Action' in game.genre
        assert game.stock_quantity == 100
    
    def test_game_default_values(self):
        """Test game with default values"""
        game = Game(game_id='test', title='Test')
        
        assert game.genre == []
        assert game.platform == []
        assert game.game_id == 'test'

class TestSecurity:
    """Test security utilities"""
    
    def test_password_length(self):
        """Test various password lengths"""
        short_pass = "123"
        long_pass = "a" * 100
        
        short_hash = hash_password(short_pass)
        long_hash = hash_password(long_pass)
        
        assert verify_password(short_hash, short_pass) == True
        assert verify_password(long_hash, long_pass) == True
    
    def test_special_characters(self):
        """Test passwords with special characters"""
        special_pass = "p@ssw0rd!#$%"
        hashed = hash_password(special_pass)
        
        assert verify_password(hashed, special_pass) == True
        assert verify_password(hashed, "p@ssw0rd") == False