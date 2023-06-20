import requests
import xml.etree.ElementTree as ET
import sys
import MovieClasses

def GetPlexMovies(plex_api_url):
    #Return a list of all movies found on plex
    
    plex_movies = []
    movies = []
    
    # Plex API request to get a list of movies
    plex_response = requests.get(plex_api_url)

    if plex_response.status_code == 200:
        # Parse XML response
        root = ET.fromstring(plex_response.content)

        # Extract Plex movies
        for movie in root.findall('.//Video'):
            #sense check
            title_element = movie.attrib['title']
            if title_element != '':
                #add it to our list of owned movies
                plex_movies.append(movie)
                
                movies.append(MovieClasses.Movie(movie.attrib))
                
        return movies
    
    else:
        print("Error retrieving movie metadata.")
        print(f"Response code: {plex_response.status_code}")
        print(f"Response content: {plex_response.content}")
        sys.exit()