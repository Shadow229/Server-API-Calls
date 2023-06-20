import random

import config
import MovieExclusions
import MovieFunctions
import Overseerr
import Plex
import TMDB

# This script will auto download movies using Overseerr. This assumes that overseer is set up and working to send your requests to radarr and ultimately onto plex.
# It will grab all movies from TMDB based on the criteria below - default is a rating of 7 or above, with a minimum of 10k votes.
# It then cross references those with whats currently available on Plex and whats listed in the exclusions file, then picks 5 random titles and sends them to overseerr as a request.


#custom tmdb search settings
rating_threshold = 7
minimum_reviews = 10000
#popularity_threshold = 100.00 - this isn't set up from an API side yet. ticket here: https://trello.com/c/xuS4lvQ0/7-add-popularity-filter-to-discover

#how many movies to get each run
download_count = 5

#moves to exclude
movie_exclusions = MovieExclusions.Exclusions


############################################################
##  Get Movie List from TMDB
############################################################

tmdb_movies = TMDB.GetTMDBMovies(config.tmdb_api_key, rating_threshold, minimum_reviews)

############################################################
##  Get Movie List from Plex
############################################################

plex_movies = Plex.GetPlexMovies(config.plex_api_url + config.plex_api_request + config.plex_token)

############################################################
##  Prepare Final List
############################################################

#Compare and remove existing titles
tmdb_movies_not_in_plex = [movie for movie in tmdb_movies if not any(MovieFunctions.compare_movies(movie, movieB.details) for movieB in plex_movies)]

#Compare and remove exclusions from previous downloads
tmdb_movies_not_in_exclusions = [movie for movie in tmdb_movies_not_in_plex if not any(MovieFunctions.compare_movies(movie, movieB) for movieB in movie_exclusions)]

############################################################
##  Download a selection of the missing titles with Overseer
############################################################

#get random movies from available list
movies_to_download = random.sample(tmdb_movies_not_in_exclusions, download_count)

#print all the movies to the terminal (debugging)
for movie in movies_to_download:
    movie_title = movie.get('title', '')
    print(f'Movie: "{movie_title}"', flush=True)

# Download movies using the Overseerr API
Overseerr.DownloadMovies(config.overseerr_api_key, config.overseerr_url, movies_to_download)