import datetime

import requests

import config

import options
from MovieManager import Movie


class TMDBMovie(Movie):
    def __init__(self, details):
        super().__init__(details)
        self.originalTitle = details.get("original_title")        
        self.year  = datetime.datetime.strptime(details['release_date'], '%Y-%m-%d').year   
        self.id = int(details.get("id"))


class TMDB():

    def __init__(self):
        self.url = config.tmdb_url
        self.api_key = config.tmdb_api_key
        
        self.movies =  []
        #self.genres = self.populate_genre_ids()
        self.excluded_genres = self.get_genre_id_list()
        
    def add_movie(self, movie: TMDBMovie):
        self.movies.append(movie)

    def GetMovies(self):
        
        print("Getting TMDB Movies")
        
        params = {
        "api_key": self.api_key,
        "certification_country": "US",
        "language": "en-US",
        "without_genres": f"{self.excluded_genres}",  # Exclude genres with IDs 28, 12, and 16
        "vote_average.gte": f"{options.rating_threshold}",  # Movies with a rating of 7 or above
        "vote_count.gte":f"{options.minimum_reviews}",
        "include_adult": False,  # Exclude adult movies
        }
               
        tmdb_response = requests.get(f"{self.url}/discover/movie", params=params)     
        max_pages = tmdb_response.json().get('total_pages')

        #loop through all pages and pull all the movies matching the criteria
        for page in range(1, max_pages +1):
            
            params["page"] = page
            
            #send the request to the tmdb API 
            tmdb_response = requests.get(f"{self.url}/discover/movie", params=params)
            
            status = tmdb_response.status_code
            
            #validity check of the status
            if status != 200:
                continue;
            
            #add the movies to our tmdb movie list
            tmdb_page = tmdb_response.json().get('results', [])
           # tmdb_movies.extend(tmdb_page)
            
            for movie in tmdb_page:
                self.add_movie(TMDBMovie(movie))
            
            #movies = ConvertToMovieType(tmdb_movies)
            


    def GetInfoFromTitle(self, movieName, year = 0):
        
        search_url = f'{config.tmdb_url}/search/movie'
        params = {
            'api_key': self.api_key,
            'query': movieName
        }
        
        if year > 0:
            params['year'] = year
        
        response = requests.get(search_url, params=params)
        
        if response.status_code == 200:
            data = response.json().get("results", [])
            
            #sort by release date -- only used if no release year is passed in and identical name match is returned
            sorted_movies = sorted(data, key=lambda movie: movie.get("release_date", ""), reverse=True)
            
            #remove case sensitvitiy on matching
            movieName = movieName.upper()
            
            #try and filter to a specific movie title
            filtered_items = [item for item in sorted_movies if item['title'].upper() == movieName or item['original_title'].upper() == movieName]
            
            Selectedmovie = {}
            
            #take the most recent release date
            if filtered_items:
                Selectedmovie = filtered_items[0]
            elif sorted_movies:
                Selectedmovie = sorted_movies[0]
                
            if Selectedmovie:
                return Selectedmovie
            
        print(f"No TMDB Movie Details Found for: {movieName}")
        return None
    
    
    
    def GetMovieDetails(self, movieName, year = 0):
            
        if isinstance(movieName, str):
            #handle a single movie
            details = self.GetInfoFromTitle(movieName, year)
            self.add_movie(TMDBMovie(details))
        elif isinstance(movieName, list):
            #handle a list of movies        
            for item in movieName:
                details = self.GetInfoFromTitle(item, year)  
                if details:
                    self.add_movie(TMDBMovie(details))     
        else:
            print("Invalid Input")


    def GetInfoFromID(self, movie_id):
        
        url = f"{config.tmdb_url}movie/{movie_id}"
        
        params = {
            "api_key": self.api_key
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            movie_data = response.json()
            self.add_movie(TMDBMovie(movie_data))     
        else:
            print("Movie not found")
        
        
    @staticmethod
    def populate_genre_ids(self):

        genre_url = f"{self.url}/genre/movie/list"
        
        params = {
            "api_key": self.api_key,
        }

        response = requests.get(genre_url, params=params)
        data = response.json()

        genres = []


        if "genres" in data:
            genres = data["genres"]
            for genre in genres:
                genre_id = genre["id"]
                genre_name = genre["name"]
                print(f"Genre ID: {genre_id}, Genre Name: {genre_name}")
                
        return genres
            
    
    def get_genre_id_list(self):
        
        genre_ids = []      

        for genre in options.exclude_genres:
            genre_ids.append(str(genre.value))
            
        genre_ids_str = ",".join(genre_ids)
        
        return genre_ids_str