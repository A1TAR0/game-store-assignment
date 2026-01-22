import functions_framework
from flask import jsonify

@functions_framework.http
def recommend_games(request):
    """
    Cloud Function to recommend games based on user preferences.
    
    This is a simple rule-based recommendation system.
    In production, you could use ML models or more sophisticated algorithms.
    """
    
    request_json = request.get_json(silent=True)
    
    if not request_json:
        return jsonify({'error': 'No data provided'}), 400
    
    # Get user preferences
    favorite_genres = request_json.get('genres', [])
    favorite_platforms = request_json.get('platforms', [])
    budget = request_json.get('budget', 100)
    
    # Sample game database (in production, query from Firestore)
    all_games = [
        {
            'id': 'elden-ring',
            'title': 'Elden Ring',
            'genre': ['Action', 'RPG'],
            'platform': ['PC', 'PlayStation', 'Xbox'],
            'price': 49.99,
            'rating': 4.8
        },
        {
            'id': 'fifa-24',
            'title': 'EA SPORTS FC 24',
            'genre': ['Sports'],
            'platform': ['PC', 'PlayStation', 'Xbox'],
            'price': 59.99,
            'rating': 4.0
        },
        {
            'id': 'baldurs-gate-3',
            'title': "Baldur's Gate 3",
            'genre': ['RPG', 'Strategy'],
            'platform': ['PC', 'PlayStation'],
            'price': 59.99,
            'rating': 4.9
        }
    ]
    
    # Score games based on preferences
    recommendations = []
    for game in all_games:
        score = 0
        
        # Check genre match
        genre_match = any(g in game['genre'] for g in favorite_genres)
        if genre_match:
            score += 3
        
        # Check platform match
        platform_match = any(p in game['platform'] for p in favorite_platforms)
        if platform_match:
            score += 2
        
        # Check budget
        if game['price'] <= budget:
            score += 1
        
        # Add rating bonus
        score += game['rating']
        
        if score > 0:
            recommendations.append({
                'game': game,
                'score': score,
                'reason': generate_reason(game, favorite_genres, favorite_platforms)
            })
    
    # Sort by score
    recommendations.sort(key=lambda x: x['score'], reverse=True)
    
    # Return top 5
    return jsonify({
        'recommendations': recommendations[:5],
        'preferences': {
            'genres': favorite_genres,
            'platforms': favorite_platforms,
            'budget': budget
        }
    }), 200

def generate_reason(game, genres, platforms):
    """Generate recommendation reason"""
    reasons = []
    
    if any(g in game['genre'] for g in genres):
        matched_genres = [g for g in game['genre'] if g in genres]
        reasons.append(f"Matches your interest in {', '.join(matched_genres)}")
    
    if any(p in game['platform'] for p in platforms):
        reasons.append(f"Available on your preferred platforms")
    
    if game['rating'] >= 4.5:
        reasons.append("Highly rated by players")
    
    return ' • '.join(reasons) if reasons else "Popular choice"