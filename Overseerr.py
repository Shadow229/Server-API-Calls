import requests
import config



class Overseerr():
    def __init__(self):
        self.url = config.overseerr_url
        self.api_key = config.overseerr_api_key
        self.root_folder = config.overseerr_root_folder
        #self.collectionId = Plex.Plex().GetCollection()

    def DownloadMovies(self, movies_to_download):
        
        #generate a header with our API key
        headers = {"X-Api-Key": self.api_key}
        
        successfulRequests = []

        #loop throug each movie to download and send the request to overseer
        for movie in movies_to_download:
            
            # Create payload for Overseerr request
            payload = {
                'title': movie.title,
                'tmdbid': movie.id,
                'mediaId': movie.id,
                'mediaType': 'movie',
                'rootFolder': self.root_folder
            }

            # Make the request to Overseerr
            try:
                response = requests.post(f'{self.url}/request', headers=headers, json=payload)
                response.raise_for_status()
                print(f'Movie "{movie.title}" requested successfully!')
                successfulRequests.append(movie)
            except requests.exceptions.RequestException as e:
                print(f'Error requesting movie "{movie.title}": {e}')
                
        return successfulRequests
                
    def DeleteMovie(self, movie_id):
        
        delete_url = f"{self.url}/media/{movie_id}"
        headers = {"X-Api-Key": self.api_key}
            
        try:
            response = requests.delete(delete_url, headers=headers)
            response.raise_for_status()  # Check if the request was successful
            print("Movie request deleted from Overseerr successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error deleting movie request: {e}")
            
            
    def SyncMediaAvailabilty(self):

        sync_url = f"{self.url}/settings/jobs/availability-sync/run"

        headers = {"X-Api-Key": self.api_key}
        response = requests.post(sync_url, headers=headers)
        
        if response.status_code == 200:
            print("Media Availability Sync triggered successfully.")
        else:
            print("Error triggering Media Availability Sync.")
        