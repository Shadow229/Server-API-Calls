import random

import options
from MovieManager import MovieManager
from Netflix import Netflix
from Overseerr import Overseerr
from Plex import Plex
from TMDB import TMDB


def update():

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
    missing_tmdb = MovieManager.compare_movies(tmdb.movies, plex.movies)
    missing_netflix = MovieManager.compare_movies(netflix.movies, plex.movies)

    #Compare and remove Exclusions
    wanted_tmdb = MovieManager.compare_movies(missing_tmdb, MovieManager.GetExclusions_List())
    wanted_netflix = MovieManager.compare_movies(missing_netflix, MovieManager.GetExclusions_List())

    ############################################################
    ##  Download titles with Overseer
    ############################################################

    #get random sample of movies from available TMDB list
    wanted_tmdb = random.sample(wanted_tmdb, min(len(wanted_tmdb), options.download_count))

    #Combine all
    movies_to_download = wanted_tmdb + wanted_netflix

    #print all the movies to the terminal (debugging)
    for movie in movies_to_download:
        print(f'Movie: "{movie.title}"', flush=True)

    # Download movies using the Overseerr API
    if movies_to_download:
        overseerr.DownloadMovies(movies_to_download)