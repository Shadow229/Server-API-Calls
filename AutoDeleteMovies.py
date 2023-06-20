import config
import MovieFunctions
import Plex

# This script will automatically delete movies from Plex, remove them from being monitored from radarr and update the overseerr availability sync job.
# It will remove any media that matches the limits below. If a movie has never been watched for 30 days, OR has been watched at least once but been idle for 730 days.
# The script will also add any removed media onto an exclusions list - which is used by the AutoGetMovies script, so removed movies aren't re-downloaded again.

# Do what you like with it - assume all the usual disclamers - ie - not my fault if you delete your entire server etc.


#Variables
IdleLimit = 730 # Days before movie will be deleted
UnWatchedLimit = 30 # Days a movie will stay on the server if downloaded but never watched

############################################################
##  Get Movie List from Plex
############################################################

plex_movies = Plex.GetPlexMovies(config.plex_api_url + config.plex_api_request + config.plex_token)

#filter to 1 movie for debugging
#moviename = "Deadpool"
#plex_movies = [item for item in plex_movies if moviename in item.title]

#debug counts
MoviesInDB = len(plex_movies)
print(f"Total Movies in Database: {MoviesInDB}")

############################################################
##  Derive Idle movies from Plex list
############################################################

#delete_list = MovieFunctions.GetIdleMovies(IdleLimit, UnWatchedLimit, plex_movies)
delete_list = plex_movies

#debug counts
MoviesToDelete = len(delete_list)
print(f"Total Movies to Delete: {MoviesToDelete}")


############################################################
##  Delete the Movies
############################################################

MovieFunctions.DeleteMovies(delete_list)