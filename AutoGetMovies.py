import random

import options
from MovieManager import MovieManager
from Netflix import Netflix
from Overseerr import Overseerr
from Plex import Plex
from TMDB import TMDB


def update():
    
    #early out
    if not options.get_netflix_top_10 and not options.auto_get_movies: return

    #create instances
    plex = Plex()
    overseerr = Overseerr()
    
    #movie lists
    tmdb = TMDB()
    netflix = TMDB()

    ############################################################
    ##  Get Movie List from TMDB
    ############################################################

    if options.auto_get_movies:
        tmdb.GetMovies()

    ############################################################
    ##  Get Movie List from Netflix
    ############################################################

    if options.get_netflix_top_10:
        netflix.GetMovieDetails(Netflix.GetTop10())

    ############################################################
    ##  Get Movie List from Plex
    ############################################################

    plex.GetMovies()
 
    ############################################################
    ##  Prepare Final Lists
    ############################################################

    #Compare and remove existing Plex titles
    missing_tmdb = MovieManager.compare_movies_uneq(tmdb.movies, plex.movies)
    missing_netflix = MovieManager.compare_movies_uneq(netflix.movies, plex.movies)    

    #Compare and remove Exclusions
    wanted_tmdb = MovieManager.compare_movies_uneq(missing_tmdb, MovieManager.GetExclusions_List())
    wanted_netflix = MovieManager.compare_movies_uneq(missing_netflix, MovieManager.GetExclusions_List())
    
    #Compare and remove existing requests that may be still downloading form prior runs
    request_tmdb = MovieManager.compare_movies_uneq(wanted_tmdb, MovieManager.GetMovies_List())
    request_netflix = MovieManager.compare_movies_uneq(wanted_netflix, MovieManager.GetMovies_List())

    ############################################################
    ##  Download titles with Overseer
    ############################################################

    #get random sample of movies from available TMDB list
    request_tmdb = random.sample(request_tmdb, min(len(request_tmdb), options.download_count))

    #Combine all
    movies_to_download = request_tmdb + request_netflix

    #print all the movies to the terminal (debugging)
    for movie in movies_to_download:
        print(f'Movie: "{movie.title}"', flush=True)

    # Download movies using the Overseerr API
    if movies_to_download:
        successfulRequests = overseerr.DownloadMovies(movies_to_download)
        
        for movie in successfulRequests:
            MovieManager.AddDownloaded(movie)