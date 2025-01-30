from auth import Auth
import requests

class One_Drive:
    def __init__(self):
        self.auth = Auth()
        #self.access_token = self.auth.get_fixed_access_token()
        self.access_token = str(open("token.key", "r+").read())
        self.filmes_folder_id = "1642E726B682B518!72464"
    
    def refresh_access_token(self):
        self.access_token = self.auth.get_fixed_access_token()
        with open("token.key", "w+") as f:
            f.write(self.access_token)
        
    def create_main_folder(self, folder):
        url = f'https://graph.microsoft.com/v1.0/me/drive/items/{self.filmes_folder_id}/children'
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            "name": folder,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }

        req = requests.post(url, headers=headers, json=data)
        
        data = req.json()
        
        if "error" in data:
            if data["error"]["code"] == "InvalidAuthenticationToken":
                self.refresh_access_token()
                return self.create_main_folder(folder)
        
        return data["id"]
    
    def create_movie_file(self):
        pass
    
    def get_folder_items(self, folder_id):
        url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }

        req = requests.get(url, headers=headers)
        
        data = req.json()
        
        if "error" in data:
            if data["error"]["code"] == "InvalidAuthenticationToken":
                self.refresh_access_token()
                return self.get_folder_items(folder_id)
        
        return data["value"]
    
    def get_downloads_frames_links(self, folder_id):
        files = self.get_folder_items(folder_id)
        
        links = []
        
        for file in files:
            if "@microsoft.graph.downloadUrl" in file:
                links.append(file["@microsoft.graph.downloadUrl"])
        
        return links
    
    def download_file(self, file_id):
        url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        download_url = response.json().get("@microsoft.graph.downloadUrl")
        if not download_url:
            raise ValueError("Não foi possível obter a URL de download.")
        
        # Baixar o vídeo
        video_response = requests.get(download_url, stream=True)
        video_response.raise_for_status()
        
        with open("video.webm", "wb") as file:
            for chunk in video_response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Download concluído!")
    
if __name__ == "__main__":
    starter = One_Drive()
    #folder_id = starter.create_main_folder("Sonserina")
    #print(folder_id)
    
    #starter.download_file()
    print(starter.get_downloads_frames_links(starter.filmes_folder_id))