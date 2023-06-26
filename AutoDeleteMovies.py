import options
from MovieManager import MovieManager
from Plex import Plex


def update():
    
    if not options.auto_delete_movies: return
    
    #instances
    plex = Plex()

    ############################################################
    ##  Get Movie List from Plex
    ############################################################

    plex.GetMovies()

    #filter to 1 movie for debugging
    #moviename = "Riddick"
    #plex_movies = [item for item in plex_movies if moviename in item.title]


    ############################################################
    ##  Derive Idle movies from Plex list
    ############################################################

    delete_list = plex.GetIdleMovies()

    #debug count
    print(f"Total Movies to Delete: {len(delete_list)}")


    ############################################################
    ##  Delete the Movies
    ############################################################

    MovieManager.DeleteMovies(delete_list)
