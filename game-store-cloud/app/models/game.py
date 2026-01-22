from app.utils.db_firestore import db

class Game:
    def __init__(self, game_id=None, title=None, description=None, price=None, 
                 publisher=None, genre=None, platform=None, image_url=None, 
                 rating=None, stock_quantity=None):
        self.game_id = game_id
        self.title = title
        self.description = description
        self.price = price
        self.publisher = publisher
        self.genre = genre or []
        self.platform = platform or []
        self.image_url = image_url
        self.rating = rating
        self.stock_quantity = stock_quantity
    
    def save(self):
        """Save game to Firestore"""
        game_ref = db.collection('games').document(self.game_id)
        game_ref.set({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'publisher': self.publisher,
            'genre': self.genre,
            'platform': self.platform,
            'image_url': self.image_url,
            'rating': self.rating,
            'stock_quantity': self.stock_quantity
        })
        return self.game_id
    
    @staticmethod
    def get_all():
        """Get all games from Firestore"""
        games_ref = db.collection('games')
        games = []
        
        for doc in games_ref.stream():
            game_data = doc.to_dict()
            game = Game(
                game_id=doc.id,
                title=game_data.get('title'),
                description=game_data.get('description'),
                price=game_data.get('price'),
                publisher=game_data.get('publisher'),
                genre=game_data.get('genre'),
                platform=game_data.get('platform'),
                image_url=game_data.get('image_url'),
                rating=game_data.get('rating'),
                stock_quantity=game_data.get('stock_quantity')
            )
            games.append(game)
        
        return games
    
    @staticmethod
    def find_by_id(game_id):
        """Find game by ID"""
        doc_ref = db.collection('games').document(game_id)
        doc = doc_ref.get()
        
        if doc.exists:
            game_data = doc.to_dict()
            return Game(
                game_id=doc.id,
                title=game_data.get('title'),
                description=game_data.get('description'),
                price=game_data.get('price'),
                publisher=game_data.get('publisher'),
                genre=game_data.get('genre'),
                platform=game_data.get('platform'),
                image_url=game_data.get('image_url'),
                rating=game_data.get('rating'),
                stock_quantity=game_data.get('stock_quantity')
            )
        return None