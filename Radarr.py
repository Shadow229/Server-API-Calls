
import requests

def remove_movie_from_radarr(base_url, api_key, movie_name, movie_year = 0):
    # Prepare the headers with the API key
    
    #
    movie_id = None

    # Search for the movie by name
    search_url = f'{base_url}/movie/lookup'
    params = {
        'term': movie_name,
    }
    response = requests.get(search_url, headers={'X-Api-Key': api_key}, params=params)
    
    # Check if the search was successful
    if response.status_code == 200:
        search_results = response.json()
        if search_results:
            # Get the first search result (assuming it's the closest match)
            
            #loop if we've passed a date
            if int(movie_year) > 0:
                # Filter the movies based on the desired year
                movies_year_filtered = [movie for movie in search_results if movie['year'] == movie_year]

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
                print(f'Movie "{movie_name}" not currently monitored.')
                return
            
            # Remove the movie using the movie ID
            remove_url = f'{base_url}/movie/{movie_id}'
            response = requests.delete(remove_url, headers={'X-Api-Key': api_key})
            
            # Check the response status
            if response.status_code == 200:
                print(f'Movie "{movie_name}" successfully removed from Radarr.')
            else:
                print(f'Failed to remove movie "{movie_name}" from Radarr:', response.status_code)
        else:
            print(f'No search results found for movie "{movie_name}".')
    else:
        print('Failed to perform the movie search in Radarr:', response.status_code)