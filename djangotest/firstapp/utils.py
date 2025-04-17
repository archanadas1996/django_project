import json
from datetime import datetime, timedelta

def get_recently_viewed(request, movie_id=None):
    """
    Get or update recently viewed movies from cookies
    """
    # Get the cookie value
    recently_viewed = request.COOKIES.get('recently_viewed', '[]')
    
    try:
        # Parse the cookie value
        viewed_movies = json.loads(recently_viewed)
        
        # If a new movie is being viewed
        if movie_id:
            # Remove the movie if it already exists
            viewed_movies = [m for m in viewed_movies if m['id'] != movie_id]
            
            # Add the new movie at the beginning
            viewed_movies.insert(0, {
                'id': movie_id,
                'timestamp': datetime.now().isoformat()
            })
            
            # Keep only the last 5 movies
            viewed_movies = viewed_movies[:5]
        
        return viewed_movies
    except json.JSONDecodeError:
        return []

def set_recently_viewed_cookie(response, viewed_movies):
    """
    Set the recently viewed cookie
    """
    # Convert to JSON
    cookie_data = json.dumps(viewed_movies)
    
    # Set cookie with 30 days expiry
    response.set_cookie(
        'recently_viewed',
        cookie_data,
        max_age=30*24*60*60,  # 30 days in seconds
        httponly=True,
        samesite='Lax'
    )
    
    return response 