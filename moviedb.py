import requests
import os

class MovieDB:
    def __init__(self):
        self.absolut_path = os.path.dirname(os.path.abspath(__file__))
        self.access_token = open(f"{self.absolut_path}/token_moviedb.key", "r+").read()
        
    def find_movie_by_id(self, movieId):
        url = f"https://api.themoviedb.org/3/movie/{movieId}?language=pt-BR"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }
        
        req = requests.get(url, headers=headers)
        
        data = req.json()
        
        name = data["title"]
        backdrop = data["backdrop_path"]
        poster = data["poster_path"]
        
        return name, backdrop, poster
    
    def get_images_by_id(self, movieId):
        url = f"https://api.themoviedb.org/3/movie/{movieId}/images"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }
        
        req = requests.get(url, headers=headers)
        
        data = req.json()
        
        poster = data["posters"][0]["file_path"]
        backdrop = data["backdrops"][0]["file_path"]
        
        for p in data["posters"]:
            if p["iso_639_1"] == "pt":
                poster = p["file_path"]

        for p in data["backdrops"]:
            if p["iso_639_1"] == "pt":
                backdrop = p["file_path"]
        
        return poster, backdrop
    

if __name__ == "__main__":
    starter = MovieDB()
    name, backdrop, poster = starter.find_movie_by_id(615)
    print(name)
    print(backdrop)
    print(poster)