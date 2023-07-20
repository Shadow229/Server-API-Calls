
#plex config
plex_api_url = 'http://192.168.111.101:32400'  #change to your Plex API URL
plex_api_request = '/library/sections/1/all' #the api request 
plex_token = '<YOUR PLEX TOKEN>' #change to your token for auth

#radarr config
radarr_url = 'http://192.168.111.101:7878/api/v3' #change to your Radarr API URL
radarr_api_key = '<YOUR RADARR API KEY>' #change to your Radarr API key

#overseerr config
overseerr_url = 'http://192.168.111.101:5055/api/v1'  #change to your Overseerr URL
overseerr_api_key = '<YOUR OVERSEERR API KEY>'  #change to your Overseerr API key
overseerr_root_folder = '/media' #change to your radarr root folder

#The Movie Database
tmdb_url = 'https://api.themoviedb.org/3/'
tmdb_api_key = '<YOUR TMDB API KEY>'  #change to your TMDB API key

#File location
script_dir = '/mnt/user/Scripts/' #set to the share the scripts are saved on. Set to '' if testing from VSCode