from constants import NetflixLocation
from constants import Genres

######################################################
# AUTO DELETE PARAMETERS
######################################################

#Do you want to auto delete movies?
auto_delete_movies = True

#determins wether the auto delete looks at the entire library on Plex. Set to False, it will only check the movies the script has downloaded itself. (see list AutoGetMovieList.py)
auto_delete_FullLibrary = False

#--------------------------------------#

#Removal Limits:
idleLimit = 730 # Days before movie will be deleted
unwatchedLimit = 30 # Days a movie will stay on the server if downloaded but never watched

#Adds any removed titles to an exclusions list to stop the auto get script picking them again in the future
UniqueFetch = True 



######################################################
# AUTO DOWNLOAD PARAMETERS
######################################################

#Do you want to auto downloaded a selection of movies from TMDB?
auto_get_movies = True

#--------------------------------------#

#TMDB search settings
rating_threshold = 7
minimum_reviews = 10000
exclude_genres = []     # example addition: [Genres.WESTERN, Genres.WAR, Genres.THRILLER]
#popularity_threshold = 100.00 - this isn't set up from an API side yet. ticket here: https://trello.com/c/xuS4lvQ0/7-add-popularity-filter-to-discover

#how many movies to get each run
download_count = 5



######################################################
# NETFLIX PARAMETERS
######################################################

#Do you want the netflix top 10?
get_netflix_top_10 = True

#--------------------------------------#

#Top 10 location
netflix_loc = NetflixLocation.UK