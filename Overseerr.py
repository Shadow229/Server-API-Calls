import requests

def DownloadMovies(api_key, overseerr_url, movies_to_download):
    
    #generate a header with our API key
    headers = {"X-Api-Key": api_key}

    #loop throug each movie to download and send the request to overseer
    for movie in movies_to_download:
        
        #get the basic info
        movie_title = movie.get('title', '')
        tmdb_id = movie.get('id', '')

        # Create payload for Overseerr request
        payload = {
            'title': movie_title,
            'tmdbid': tmdb_id,
            'mediaId': tmdb_id,
            'mediaType': 'movie',
            'rootFolder':'/media'
        }

        # Make the request to Overseerr
        try:
            response = requests.post(f'{overseerr_url}/request', headers=headers, json=payload)
            response.raise_for_status()
            print(f'Movie "{movie_title}" requested successfully!', flush=True)
        except requests.exceptions.RequestException as e:
            print(f'Error requesting movie "{movie_title}": {e}')
            
            
def DeleteMovie(base_url, api_key, movie_id):
     
    delete_url = f"{base_url}/media/{movie_id}"
    headers = {"X-Api-Key": api_key}
          
    try:
        response = requests.delete(delete_url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        print("Movie request deleted from Overseerr successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error deleting movie request: {e}")
        
        
def SyncMediaAvailabilty(overseerr_url, api_key):

    sync_url = f"{overseerr_url}/settings/jobs/availability-sync/run"

    headers = {"X-Api-Key": api_key}
    response = requests.post(sync_url, headers=headers)
    
    if response.status_code == 200:
        print("Media Availability Sync triggered successfully.")
    else:
        print("Error triggering Media Availability Sync.")
    