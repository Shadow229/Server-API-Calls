from constants import NetflixLocation
from constants import Genres

######################################################
# AUTO DELETE PARAMETERS
######################################################

#Do you want to auto delete movies?
    #NOTE: Auto delete looks at ALL movies on your plex library - NOT just the ones the script downloads.
auto_delete_movies = True

#--------------------------------------#

idleLimit = 730 # Days before movie will be deleted
unwatchedLimit = 30 # Days a movie will stay on the server if downloaded but never watched


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