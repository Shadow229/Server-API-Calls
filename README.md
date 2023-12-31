# Movie-Management-APIs

Automatically Add and Remove movies from Plex

This script assumes a working stack of Plex, Overseerr and Radarr due to API calls to each endpoint.

You will also need to register an account on themoviedb.org, and request an API key (all free)

Written and tested only for an UNRAID OS. Some alteration to the usage notes below may be required for other operating systems.


The 2 main scripts are AutoDeleteMovies.py, and AutoGetMovies.py. Both work together in main.py to generate a 'churn' of movies on and off the server.

Amount of movies downloaded per run, movie rating to fetch, time before deletion, and some other settings are editable in those 2 script themselves.



Standard disclaimer before we get into the install notes - Do what you want with this. I developed it try and get some new discoveries dropping onto Plex I might not otherwise have 
personally searched for. I will take no responsibility if it breaks, deletes your server, steals your significant other, or takes over the world.




SET UP:

    1. Place all scripts onto a share on your server (I created a 'Scripts' share for this specifically)

    2. Update the config.py script with your API information and the location of the scripts

    3. Update the options.py script with your preferences for idle times, download quantities, netflix top 10 location, etc.
        
        3b. Additional check: Worth going into constraints.py and updating the name of your plex library if you havent called it 'Movies'

-- Optional: at this stage you should be able to run the scripts in vscode and test API connections and tailor the parameters if you want to.
-- Note: If testing locally, change scriptLocation in config to '' (blank string)

-- The next steps are for setting up on an UNRAID OS ONLY (Tested on v. 6.12.0) - steps will likely be vastly different on any other OS.

    4. Install Python 3

        i: Go to APPS and install NerdTools
        ii: Go to Plugins, under Installed plugins find NerdTools - click the icon
        iii: Seach for Python 3 and set it to 'ON' - hit apply.

    5. Schedule the AutoGetMovies.py and AutoDeleteMoves.py via 'main.py' with Usersripts

        i.      go to settings -> Userscripts (if this is missing you may need to install the CA userscripts - google will help you here if you're unsure about community apps)
        ii.     Click 'Add new script', give it an appropriate name add the following line of code (change for the share path you placed the files):

            #!/bin/bash

            /usr/bin/python3 /mnt/user/Scripts/main.py

        iii: Save changes
    

-- You can test run the script manually at this point by clicking 'Run Script'.

    6. If all is good - schedule the script to run at whatever interval you wish - I'd default to weekly but depends on how often you want new movies dropping onto your system.


Enjoy!

