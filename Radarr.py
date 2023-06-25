
import requests
import config

class Radarr():

    def __init__(self):
        self.url = config.radarr_url
        self.api_key = config.radarr_api_key
        
        
    def getID(self, movie):
               
        # Search for the movie first by tmdb to get official name just in case
        search_url = f'{self.url}/movie/lookup/tmdb'
        params = {
            'tmdbId': movie.id,
        }
        id_response = requests.get(search_url, params=params, headers={'X-Api-Key': self.api_key},)
        
        # Check if the search was successful
        if id_response.status_code == 200:
            search_results = id_response.json()        
            #set movie title - or use default if None
            movie_title = search_results.get('title') or movie.title
            
        # Search for the movie by name - this seems to be the only way the radarr native ID gets returned
        search_url = f'{self.url}/movie/lookup/'
        params = {
            'term': movie_title  
        }
        tmdb_response = requests.get(search_url , params=params, headers={'X-Api-Key': self.api_key})
        
        # Check if the search was successful
        if tmdb_response.status_code == 200:
            search_results = tmdb_response.json()
            if search_results:
                
                #check for a tmdb id first - best match
                tmdbIds = [m for m in search_results if m['tmdbId'] == movie.id] 
                
                if tmdbIds:
                    return tmdbIds[0].get('id')
                
                 # if no tmdb match, loop if we've passed a date
                elif int(movie.year) > 0:      
                  # Filter the movies based on the desired year                        
                    movies_year_filtered = [movie for movie in search_results if movie['year'] == movie.year]

                    for result in movies_year_filtered:
                        try:
                            movie_id = result['id']
                            break
                        except:
                            continue  
                else:
                    #if not date passed in just loop through all the results till we find one with an ID
                    for result in search_results:
                        try:
                            movie_id = result['id']
                            break
                        except:
                            continue

                #If we can't find an ID at all - the movie isnt monitored already
                if movie_id == None:
                    print(f'Movie "{movie.title}" not currently monitored.')
                    return
            else:
                print(f'No search results found for movie "{movie.title}".')
        else:
            print('Failed to perform the movie search in Radarr:', response.status_code)
            
            


    def unmonitor(self, movie):

                #Get the radarr id
                movie_id = self.getID(movie)
                
                # Remove the movie using the movie ID
                remove_url = f'{self.url}/movie/{movie_id}'
                response = requests.delete(remove_url, headers={'X-Api-Key': self.api_key})
                
                # Check the response status
                if response.status_code == 200:
                    print(f'Movie "{movie.title}" successfully removed from Radarr.')
                else:
                    print(f'Failed to remove movie "{movie.title}" from Radarr:', response.status_code)
