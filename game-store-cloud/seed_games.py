from app.utils.db_firestore import db
from dotenv import load_dotenv

load_dotenv()

def seed_games():
    """Add sample games to Firestore"""
    
    games = [
        {
            'game_id': 'elden-ring',
            'title': 'Elden Ring',
            'description': 'A vast open-world action RPG where you explore a shattered realm filled with danger and discovery. Created by FromSoftware and George R.R. Martin.',
            'price': 49.99,
            'publisher': 'FromSoftware',
            'genre': ['Action', 'RPG', 'Adventure'],
            'platform': ['PC', 'PlayStation', 'Xbox'],
            'image_url': 'https://picsum.photos/300/400',
            'rating': 4.8,
            'stock_quantity': 100,
            'release_date': '2022-02-25'
        },
        {
            'game_id': 'god-of-war',
            'title': 'God of War Ragnarök',
            'description': 'Embark on an epic and heartfelt journey as Kratos and Atreus struggle with holding on and letting go.',
            'price': 59.99,
            'publisher': 'Sony Interactive Entertainment',
            'genre': ['Action', 'Adventure'],
            'platform': ['PlayStation', 'PC'],
            'image_url': 'https://picsum.photos/300/400',
            'rating': 4.9,
            'stock_quantity': 75,
            'release_date': '2022-11-09'
        },
        {
            'game_id': 'zelda-totk',
            'title': 'The Legend of Zelda: Tears of the Kingdom',
            'description': 'An epic adventure across the land and skies of Hyrule awaits in this sequel to Breath of the Wild.',
            'price': 54.99,
            'publisher': 'Nintendo',
            'genre': ['Action', 'Adventure', 'RPG'],
            'platform': ['Switch'],
            'image_url': 'https://picsum.photos/300/400',
            'rating': 4.9,
            'stock_quantity': 120,
            'release_date': '2023-05-12'
        },
        {
            'game_id': 'baldurs-gate-3',
            'title': "Baldur's Gate 3",
            'description': 'Gather your party and return to the Forgotten Realms in a tale of fellowship and betrayal, survival and sacrifice.',
            'price': 59.99,
            'publisher': 'Larian Studios',
            'genre': ['RPG', 'Strategy', 'Adventure'],
            'platform': ['PC', 'PlayStation', 'Xbox'],
            'image_url': 'https://picsum.photos/300/400',
            'rating': 4.9,
            'stock_quantity': 90,
            'release_date': '2023-08-03'
        },
        {
            'game_id': 'spider-man-2',
            'title': "Marvel's Spider-Man 2",
            'description': 'Spider-Men Peter Parker and Miles Morales face the ultimate test of strength as they fight to save the city.',
            'price': 69.99,
            'publisher': 'Sony Interactive Entertainment',
            'genre': ['Action', 'Adventure'],
            'platform': ['PlayStation'],
            'image_url': 'https://picsum.photos/300/400',
            'rating': 4.7,
            'stock_quantity': 85,
            'release_date': '2023-10-20'
        },
        {
            'game_id': 'starfield',
            'title': 'Starfield',
            'description': 'The first new universe in 25 years from Bethesda Game Studios. Create any character and explore with freedom.',
            'price': 69.99,
            'publisher': 'Bethesda',
            'genre': ['RPG', 'Action', 'Adventure'],
            'platform': ['PC', 'Xbox'],
            'image_url': 'https://picsum.photos/300/400',
            'rating': 4.2,
            'stock_quantity': 110,
            'release_date': '2023-09-06'
        },
        {
            'game_id': 'fifa-24',
            'title': 'EA SPORTS FC 24',
            'description': 'Experience the beautiful game with over 19,000 players, 700+ teams, and 30+ leagues in the most authentic football experience.',
            'price': 59.99,
            'publisher': 'EA Sports',
            'genre': ['Sports', 'Simulation'],
            'platform': ['PC', 'PlayStation', 'Xbox', 'Switch'],
            'image_url': 'https://picsum.photos/300/400',
            'rating': 4.0,
            'stock_quantity': 150,
            'release_date': '2023-09-29'
        },
        {
            'game_id': 'cyberpunk-2077',
            'title': 'Cyberpunk 2077',
            'description': 'An open-world action-adventure RPG set in the megalopolis of Night City. Customize your character and playstyle.',
            'price': 39.99,
            'publisher': 'CD Projekt Red',
            'genre': ['RPG', 'Action', 'Adventure'],
            'platform': ['PC', 'PlayStation', 'Xbox'],
            'image_url': 'https://picsum.photos/300/400',
            'rating': 4.5,
            'stock_quantity': 95,
            'release_date': '2020-12-10'
        }
    ]
    
    for game in games:
        game_id = game.pop('game_id')
        db.collection('games').document(game_id).set(game)
        print(f"Added: {game['title']}")
    
    print(f"\n✅ Successfully added {len(games)} games to Firestore!")

if __name__ == '__main__':
    seed_games()