import requests
import options



class Netflix():
    
    @staticmethod
    def GetTop10():
        
        location = options.netflix_loc        
        
        print(f"Getting {location.name} Netflix Top 10")

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34",
        }
          
        netflixEndpoint = f"https://www.netflix.com/tudum/top10/_next/data/vLahU6F87fyfl9CPVfvbl/{location.value}.json"
        
        NetflixScrape = requests.get(netflixEndpoint, headers=headers)
        NetflixTop10 = NetflixScrape.json()

        NetflixTop10Titles = [item['name'] for item in NetflixTop10['pageProps']['data']['weeklyTopTen']]

        #print(f"Netflix Top 10: {NetflixTop10Titles}")
        
        return NetflixTop10Titles


