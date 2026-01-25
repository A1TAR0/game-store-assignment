from app.utils.db_firestore import db
from datetime import datetime

class Wishlist:
    @staticmethod
    def add_game(user_id, game_id):
        """Add a game to user's wishlist"""
        wishlist_ref = db.collection('wishlists').document(str(user_id))
        wishlist_doc = wishlist_ref.get()
        
        if wishlist_doc.exists:
            # Update existing wishlist
            current_games = wishlist_doc.to_dict().get('games', [])
            if game_id not in current_games:
                current_games.append(game_id)
                wishlist_ref.update({
                    'games': current_games,
                    'updated_at': datetime.now()
                })
                return True
            return False  # Already in wishlist
        else:
            # Create new wishlist
            wishlist_ref.set({
                'user_id': user_id,
                'games': [game_id],
                'updated_at': datetime.now()
            })
            return True
    
    @staticmethod
    def remove_game(user_id, game_id):
        """Remove a game from user's wishlist"""
        wishlist_ref = db.collection('wishlists').document(str(user_id))
        wishlist_doc = wishlist_ref.get()
        
        if wishlist_doc.exists:
            current_games = wishlist_doc.to_dict().get('games', [])
            if game_id in current_games:
                current_games.remove(game_id)
                wishlist_ref.update({
                    'games': current_games,
                    'updated_at': datetime.now()
                })
                return True
        return False
    
    @staticmethod
    def get_user_wishlist(user_id):
        """Get all games in user's wishlist"""
        wishlist_ref = db.collection('wishlists').document(str(user_id))
        wishlist_doc = wishlist_ref.get()
        
        if wishlist_doc.exists:
            return wishlist_doc.to_dict().get('games', [])
        return []
    
    @staticmethod
    def is_in_wishlist(user_id, game_id):
        """Check if a game is in user's wishlist"""
        games = Wishlist.get_user_wishlist(user_id)
        return game_id in games