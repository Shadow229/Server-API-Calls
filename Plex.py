import datetime
import sys
import xml.etree.ElementTree as ET

import requests

import constants
import config
import options

from MovieManager import Movie, MovieManager


class PlexMovie(Movie):
    def __init__(self, details):
        super().__init__(details)
        self.originalTitle = details.get("originalTitle")        
        self.year =  int(details.get("year"))
        self.key = details.get("key")    
        self.dateAdded = datetime.datetime.fromtimestamp(int(details.get("addedAt")))

        lastViewedVal = details.get("lastViewedAt")
        self.isWatched = True
        
        self.rating_key = int(details.get("ratingKey"))
        self.id = self.setTMDBid()

        if lastViewedVal is None:
            self.isWatched = False
            self.lastViewedAt = None
        else:
            self.lastViewedAt = datetime.datetime.fromtimestamp(int(lastViewedVal))
      
             
    def setTMDBid(self):
        #if TMDB ID's are missing, be sure to select 'The Movie Database' as an Agent in Plex settings (settings->agents->films)
            
        #get metadata
        plex_movie = requests.get(f"{config.plex_api_url}/library/metadata/{self.rating_key}?X-Plex-Token={config.plex_token}")
        movie_xml = ET.fromstring(plex_movie.content)

        # Find all Guid elements
        guid_elements = movie_xml.findall('.//Guid')

        # Get the id attributes of all Guid elements
        guid_ids = [guid.get("id") for guid in guid_elements]

        #Get the tmdb ID
        for metadata in guid_ids:
            if metadata.startswith('tmdb'):
                tmdb_id = metadata.split('//')[1]
                
                #print(f"Movie: {self.title}  TMDB ID:", tmdb_id)                
                return int(tmdb_id)
       
        # Handle the case when TMDB ID is not available
        print(f"TMDB ID not found for '{self.title}'. Fix metadata in Plex")        
        return 0


class Plex():

    def __init__(self):
        self.url = config.plex_api_url
        self.token = config.plex_token
        self.idleLimit = options.idleLimit # Days before movie will be deleted
        self.unwatchedLimit = options.unwatchedLimit # Days a movie will stay on the server if downloaded but never watched
        
        self.movies: list[PlexMovie] = []        
        self.sectionId = self.GetSectionID()
            
        
    def add_movie(self, movie: PlexMovie):
        self.movies.append(movie)
        
    def GetSectionID(self):
        response = requests.get(f"{self.url}/library/sections", headers={"X-Plex-Token": self.token})
        # Check the response status code
        if response.status_code == 200:
            # Parse the XML response
            xml_data = response.text
            root = ET.fromstring(xml_data)

            # Extract the section ID
            for directory in root.iter("Directory"):
                section_id = directory.attrib.get("key")
                section_name = directory.attrib.get("title")
                if section_name == constants.PLEXLIBRARY:
                    return section_id
            print("Plex Library Name Not Found - No Section ID available")
            sys.exit()
        else:
            print("No Plex sections found - API call failed")
            sys.exit()


    def GetMovies(self):
        #Get of all movies found on plex
        
        print("Retreiving Plex Titles from Server")
           
        # Plex API request to get a list of movies
        plex_response = requests.get(f"{self.url}/library/sections/{self.sectionId}/all?X-Plex-Token={self.token}")

        if plex_response.status_code == 200:
            # Parse XML response
            root = ET.fromstring(plex_response.content)
            
            # Extract Plex movies
            for movie in root.findall('.//Video'):
                #sense check
                title_element = movie.attrib['title']
                if title_element != '':                   
                    #add it to our list of owned movies
                    newMovie = PlexMovie(movie.attrib)
                    self.add_movie(newMovie)
                    #print(newMovie.originalTitle)        
        else:
            print("Error retrieving movie metadata.")
            print(f"Response code: {plex_response.status_code}")
            print(f"Response content: {plex_response.content}")
            sys.exit()
            
            
    def GetIdleMovies(self):
        #return a list of movies that match the idle limits passed in
        
        IdleMovies = []
        
        print("Processing idle movies...")
        
        for movie in self.movies:
                
            #debugging flags for terminal printouts      
            MarkToDelete = 'False'

            #Used to calculate the idle days - overwritten below
            start_Date = datetime.date.today()  

            #calculate our idle_threshold and end date
            idle_threshold = 0
            if movie.isWatched:
                #Watched
                start_Date = movie.lastViewedAt.date()
                idle_threshold = self.idleLimit              
            else:             
                #Not watched
                start_Date = movie.dateAdded.date()
                idle_threshold = self.unwatchedLimit
    

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



    def RemoveExisting(self, v_movieList):
        [movie for movie in v_movieList if not any(MovieManager.compare_movies(movie, movieB.details) for movieB in self.movieList)]
        