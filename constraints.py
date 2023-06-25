from enum import Enum

#TMDB Genres
class Genres(Enum):
    ACTION = 28
    ADVENTURE = 12
    ANIMATION = 16
    COMEDY = 35
    CRIME = 80
    DOCUMENTARY = 99
    MYSTERY = 9648
    ROMANCE = 10749
    THRILLER = 53
    WAR = 10752
    WESTERN = 37    
    
    
#Netflix top 10 locations
class NetflixLocation(Enum):
    GLOBAL = 'index'
    UK = 'united-kingdom'
    USA = 'united-states'
    SPAIN = 'spain'
    SWEDEN = 'sweden'
    POLAND = 'poland'
    AUSTRALIA = 'australia'
    
#Plex constants
PLEXLIBRARY = "Movies" 