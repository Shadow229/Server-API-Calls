import datetime

#Class for all the exclusion details we need
class MovieExclusion:
    def __init__(self, title, year):
        self.title = title
        self.year = year

    def __str__(self):
        return f"Movie: {self.title}\nYear:{self.year}"
    
    
#Movie details split out to make referencing easier
class Movie:
    def __init__(self, details):
        self.details = details
        self.title = details["title"]
        self.originalTitle = details.get("originalTitle")        
        self.year =  int(details["year"])
        self.key = details.get("key")    
        self.ID = int(details.get("ratingKey"))
        self.dateAdded = datetime.datetime.fromtimestamp(int(details.get("addedAt")))
        
        lastViewedVal = details.get("lastViewedAt")
        self.isWatched = True

        if lastViewedVal is None:
            self.isWatched = False
            self.lastViewedAt = None
        else:
            self.lastViewedAt = datetime.datetime.fromtimestamp(int(lastViewedVal))


    def __str__(self):
        return f"Movie: {self.title}\nYear:{self.year}"