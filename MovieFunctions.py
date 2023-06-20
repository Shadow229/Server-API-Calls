
import datetime
import json

import requests

import MovieClasses
import config
import Radarr
import MovieExclusions
import Overseerr

#helper functions
def movie_exclusion_to_dict(exclusion):
    return {
        "title": exclusion.title,
        "year": exclusion.year
    }

def create_movie_exclusions(title, year):
    return {
        "title": title,
        "year": year
    }
    
    
def compare_movies(TMDB_movie, other_movie):
    #Compares 2 movies based on release year and title
     
    tmdb_date = datetime.datetime.strptime(TMDB_movie['release_date'], '%Y-%m-%d').year
    
    matching = (
            other_movie['title'] == TMDB_movie['title'] or
            other_movie['title'] == TMDB_movie['original_title']
        ) and int(other_movie['year']) == tmdb_date
    
    #if matching and TMDB_movie['title'] != TMDB_movie['original_title']:
    #    print(f"Match Found: tmdb movie: {TMDB_movie['title']} against other movie: {other_movie['title']}")
      
    return matching


def GetIdleMovies(idleLimit, UnwatchedLimit, movies: MovieClasses.Movie):
    #return a list of movies that match the idle limits passed in
    
    IdleMovies = []
    
    for movie in movies:
            
        #debugging flags for terminal printouts      
        MarkToDelete = 'False'

        #Used to calculate the idle days - overwritten below
        start_Date = datetime.date.today()  

        #calculate our idle_threshold and end date
        idle_threshold = 0
        if movie.isWatched:
            #Watched
            start_Date = movie.lastViewedAt.date()
            idle_threshold = idleLimit              
        else:             
            #Not watched
            start_Date = movie.dateAdded.date()
            idle_threshold = UnwatchedLimit
   

        # Get the idle days
        idle_days = (datetime.date.today() - start_Date).days          


        #if the movies idle threadshold is above the desired, run the delete command
        if idle_days >= idle_threshold:
            IdleMovies.append(movie)
            MarkToDelete = 'True'

            print(f"Movie: {movie.title}")
            print(f"Last active date: {start_Date}")
            print(f"Movie Watched: {str(movie.isWatched)}")
            print(f"Idle Days: {idle_days}")
            print(f"Delete: {MarkToDelete}")
            print("-----------")
        
    return IdleMovies


def AddExclusion(movie):  
    #Add the deleted movie to the exclusions so the auto downloader doesnt pick it up again
    
    exclusions = MovieExclusions.Exclusions
    
    #Create a new exclusion
    #new_exclusion = MovieClasses.MovieExclusion(movie.title, movie.year)
    new_exclusion = create_movie_exclusions(movie.title, movie.year)
    
    #add to exclusions
    exclusions.append(new_exclusion)
    
    # Save the changes to the file (script location on the server share)
    with open(f"{config.scriptLocation}/MovieExclusions.py", "w") as file:
    #with open("MovieExclusions.py", "w") as file: ##change to this if testing locally
        file.write("Exclusions = ")
        json.dump(exclusions, file, indent=4)
        print(f"Movie '{movie.title}' added to exclusions list successfully.")
        
   # MovieExclusions.Exclusions = exclusions
        
        

def DeleteMovies(delete_list, AddToExclusion: bool = True):
    #Deletes the movies from plex, and also removes the reference from Radarr so it doesn't try and grab the title again

    for movie in delete_list:
       
        # Construct the delete URL
        delete_url = f"{config.plex_api_url}{movie.key}{config.plex_token}"

        # Send the DELETE request
        response = requests.delete(delete_url)

        # Check the response status code
        if response.status_code == 200:
            print(f"Movie '{movie.title}' deleted from Plex successfully.")
        
            #Remove as a request in overseerr - this wasn't needed and only needed the media availability Sync'd
            #TMDBmovieID = TMDB.GetMovieID(config.tmdb_api_key, movie.title, movie.year)
            #Overseerr.DeleteMovie(config.overseerr_url, config.overseerr_api_key, TMDBmovieID)
            #also remove it from radarr so we don't continue to monitor for downloading
            Radarr.remove_movie_from_radarr(config.radarr_url, config.radarr_api_key, movie.title, int(movie.year))
            
        else:
            print("Error deleting the movie.")
            print(f"Response code: {response.status_code}")
            print(f"Response content: {response.content}")
            

        
        if AddToExclusion:
            AddExclusion(movie)
            

    #Sync the media availability from overseerr so it can be redownloaded if wanted
    Overseerr.SyncMediaAvailabilty(config.overseerr_url, config.overseerr_api_key) 