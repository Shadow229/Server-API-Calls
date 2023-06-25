
import json

import requests

import config
from Radarr import Radarr
import MovieExclusions
import Overseerr


#Movie details split out to make referencing easier
class Movie:
    def __init__(self, details):
        self.details = details
        self.title = details["title"]

    def __str__(self):
        return f"Movie: {self.title}"


#Class for all the exclusion details we need
class MovieExclusion:
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return f"Movie: {self.title}\nYear:{self.year}"
    

#General Functions for movie management
class MovieManager():
    
    exclusions = MovieExclusions.Exclusions
    
    def GetExclusions():
        return MovieManager.exclusions
    
    #helper functions

    def create_movie_exclusion(exclusion):
        return {
            "title": exclusion.title,
            #"year": exclusion.year,
            "id": exclusion.id #tmdb id
        }

        
        
    def compare_movies(list1, list2):
        #compare 2 movie lists based on TMDB ID
        return [movie for movie in list1 if not any(MovieManager.compare_movie_ids(movie.id, movieB.id) for movieB in list2)]

    def compare_movie_ids(ID1, ID2):
        #Compared 2 movies based on TMDB ID
        return int(ID1) == int(ID2)    

    def compare_movie_titles(Movie1, Movie2):
        #Compares 2 movies based on release year and title
        
        #Remove Case Sensitivity
        MT1 = Movie1.title.upper()
        MT2 = Movie2.title.upper()
        OT1 = Movie1.originalTitle.upper()
        OT2 = Movie2.originalTitle.upper()
        
        matching = (
                MT1 == MT2 or
                MT1 == OT2 or
                OT1 == MT2 or
                OT1 == OT2            
            ) and int(Movie1.year) == int(Movie2.year)
        
        return matching



    def AddExclusion(movie):  
        #Add the deleted movie to the exclusions so the auto downloader doesnt pick it up again
        
        exclusions = MovieExclusions.Exclusions
        
        #Create a new exclusion
        #new_exclusion = MovieClasses.MovieExclusion(movie.title, movie.year)
        new_exclusion = MovieManager.create_movie_exclusion(movie)
        
        #add to exclusions
        exclusions.append(new_exclusion)
        
        # Save the changes to the file (script location on the server share)
        with open(f"{config.script_dir}MovieExclusions.py", "w") as file:
        #with open("MovieExclusions.py", "w") as file: ##change to this if testing locally
            file.write("Exclusions = ")
            json.dump(exclusions, file, indent=4)
            print(f"Movie '{movie.title}' added to exclusions list successfully.")
                        
            

    def DeleteMovies(delete_list, AddToExclusion: bool = True):
        #Deletes the movies from plex, and also removes the reference from Radarr so it doesn't try and grab the title again

        for movie in delete_list:
        
            # Construct the delete URL
            delete_url = f"{config.plex_api_url}{movie.key}?X-Plex-Token={config.plex_token}"

            # Send the DELETE request
            response = requests.delete(delete_url)

            # Check the response status code
            if response.status_code == 200:
                print(f"Movie '{movie.title}' deleted from Plex successfully.")

                #also remove it from radarr so we don't continue to monitor for downloading
                Radarr().unmonitor(movie)
                
            else:
                print("Error deleting the movie.")
                print(f"Response code: {response.status_code}")
                print(f"Response content: {response.content}")
                
                        
            if AddToExclusion:
                MovieManager.AddExclusion(movie)
                

        #Sync the media availability from overseerr so it can be redownloaded if wanted
        Overseerr.SyncMediaAvailabilty(config.overseerr_url, config.overseerr_api_key) 
        
