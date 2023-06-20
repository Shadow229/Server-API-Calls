import requests
import config

def GetTMDBMovies(tmdb_api_key, rating_threshold, minimum_reviews):
    
    tmdb_movies = []
    max_pages = 500 # set to max initially
    
    #TMDB Request Params
    mainURL =  f'{config.tmdb_url}discover/movie?api_key={tmdb_api_key}\
    &certification_country=US\
    &language=en-US\
    &vote_average.gte={rating_threshold}\
    &vote_count.gte={minimum_reviews}'
    #&popularity.gte={popularity_threshold}\ -- not currently included in the api - ticket here: https://trello.com/c/xuS4lvQ0/7-add-popularity-filter-to-discover

    mainURL = mainURL.replace(" ", "") #remove whitespace

    #get max pages of the request so we know our loop range
    tmdb_api_url = f'{mainURL}&page={max_pages}'
    tmdb_response = requests.get(tmdb_api_url)
    max_pages = tmdb_response.json().get('total_pages')

    #loop through all pages and pull all the movies matching the criteria
    for page in range(1, max_pages +1):
        
        #send the request to the tmdb API
        tmdb_api_url = f'{mainURL}&page={page}'   
        tmdb_response = requests.get(tmdb_api_url)
        
        status = tmdb_response.status_code
        
        #validity check of the status
        if status != 200:
            continue;
        
        #add the movies to our tmdb movie list
        tmdb_page = tmdb_response.json().get('results', [])
        tmdb_movies.extend(tmdb_page)
        
    return tmdb_movies


def GetMovieID(api_key, movieName, year = 0):

    search_url = f'{config.tmdb_url}search/movie'
    params = {
        'api_key': api_key,
        'query': movieName
    }
    
    if year > 0:
        params['year'] = year
    
    response = requests.get(search_url, params=params)
    data = response.json()

    if 'results' in data and data['results']:
        movie = data['results'][0]
        return movie['id']

    return None
