
import json

import requests

import config
from Radarr import Radarr
import MovieExclusions
import AutoGetMovieList
from Overseerr import Overseerr


#Movie details split out to make referencing easier
class Movie:
    def __init__(self, details):
        self.details = details
        self.title = details["title"]

    def __str__(self):
        return f"Movie: {self.title}"


#Short Class for all movie list details we need
class MovieListTag:
    def __init__(self, title, id):
        self.title = title
        self.id = id

    def __str__(self):
        return f"Movie: {self.title}\nID:{self.id}"
    

#General Functions for movie management
class MovieManager():
    
    exclusions = MovieExclusions.Exclusions
    movieList = AutoGetMovieList.MovieList
    
    def GetExclusions_Dict():              
        return MovieManager.exclusions
    
    
    def GetExclusions_List():        
        return MovieManager.generate_movie_list_from_dict(MovieManager.exclusions)

    def GetMovies_List():        
        return MovieManager.generate_movie_list_from_dict(MovieManager.movieList)
                
    
    #helper functions

    def create_movie_record_entry(movie):
        return {
            "title": movie.title,
            #"year": exclusion.year,
            "id": movie.id #tmdb id
        }
        
        
 
    #generate a list from the dict file
    def generate_movie_list_from_dict(movie_dict):
        exclusions_list = []
        
        for exclusion_data in movie_dict:
            title = exclusion_data["title"]
            id = exclusion_data["id"]
            exclusion = MovieListTag(title, id)
            exclusions_list.append(exclusion)
            
        return exclusions_list


    def compare_movies_eq(list1, list2):
        #compare 2 movie lists based on TMDB ID
        #Return any of list1 contained in list2
        return [movie for movie in list1 if any(MovieManager.compare_movie_ids(movie.id, movieB.id) for movieB in list2)]
            
    def compare_movies_uneq(list1, list2):
        #compare 2 movie lists based on TMDB ID
        #Return all of list1 NOT IN list2
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



    # def AddExclusion(movie):  
    #     #Add the deleted movie to the exclusions so the auto downloader doesnt pick it up again
        
    #     exclusions = MovieExclusions.Exclusions
        
    #     #Create a new exclusion
    #     #new_exclusion = MovieClasses.MovieExclusion(movie.title, movie.year)
    #     new_exclusion = MovieManager.create_movie_record_entry(movie)
        
    #     #add to exclusions
    #     exclusions.append(new_exclusion)
        
    #     # Save the changes to the file (script location on the server share)
    #     with open(f"{config.script_dir}MovieExclusions.py", "w") as file:
    #     #with open("MovieExclusions.py", "w") as file: ##change to this if testing locally
    #         file.write("Exclusions = ")
    #         json.dump(exclusions, file, indent=4)
    #         print(f"Movie '{movie.title}' added to exclusions list successfully.")
                        
                  
    def AddExclusion(movie):
        #Add the deleted movie to the exclusions so the auto downloader doesnt pick it up again
        
        fileTitle = 'MovieExclusions'
        jsonTitle = 'Exclusions'
        exclusions = MovieExclusions.Exclusions  

        #add movie to exclusions list
        MovieManager.AddMovieToList(movie, exclusions, fileTitle, jsonTitle)
              
    def AddDownloaded(movie):
        #Add the movie to the movie list to track what is downloaded by the script
        
        fileTitle = 'AutoGetMovieList'
        jsonTitle = 'MovieList'
        movieList = AutoGetMovieList.MovieList  
        
        #add movie to exclusions list
        MovieManager.AddMovieToList(movie, movieList, fileTitle, jsonTitle)      
        
        
    def RemoveDownloaded(movie):
        #Add the movie to the movie list to track what is downloaded by the script
        
        fileTitle = 'AutoGetMovieList'
        jsonTitle = 'MovieList'
        movieList = AutoGetMovieList.MovieList  

        #add movie to movie list
        MovieManager.RemoveMovieFromList(movie, movieList, fileTitle, jsonTitle)
              
                                          
    def AddMovieToList(movie, movieList, fileTitle, jsonTitle):  
        #Add the movie and tmdb ID to a list
         
        #Create a new movie entry
        new_movie = MovieManager.create_movie_record_entry(movie)
        
        #add to list
        movieList.append(new_movie)
        
        MovieManager.writeMovielistToFile(movie, movieList, fileTitle, jsonTitle)
            
            
    def RemoveMovieFromList(movie, movieList, fileTitle, jsonTitle):
        #remove from movielist
        #ActualListofMovies = MovieManager.generate_movie_list_from_dict(movieList)
                
        newList = [movie2 for movie2 in movieList if movie2["id"] != movie.id]
   
        MovieManager.writeMovielistToFile(movie, newList, fileTitle, jsonTitle)
            


    def writeMovielistToFile(movie, movieList, fileTitle, jsonTitle):
        # Save the changes to the file (script location on the server share)
        #with open(f"{config.script_dir}{fileTitle}.py", "w") as file:
        with open(f"{fileTitle}.py", "w") as file: ##change to this if testing locally
            file.write(f"{jsonTitle} = ")
            json.dump(movieList, file, indent=4)
            print(f"Movie '{movie.title}' added to {fileTitle} list successfully.")



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
            MovieManager.RemoveDownloaded(movie)
                

        #Sync the media availability from overseerr so it can be redownloaded if wanted
        Overseerr().SyncMediaAvailabilty() 
        
