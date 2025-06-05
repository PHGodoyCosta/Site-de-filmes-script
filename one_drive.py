from auth import Auth
from utils import Utils
import os
import requests
import json

class One_Drive:
    def __init__(self):
        self.auth = Auth()
        self.utils = Utils()
        #self.access_token = self.auth.get_fixed_access_token()
        self.absolut_path = os.path.dirname(os.path.abspath(__file__))
        self.access_token = str(open(f"{self.absolut_path}/token.key", "r+").read())
        self.preload = self.preload = json.loads(open(f"{self.absolut_path}/preload.json", "r+").read())
        self.filmes_folder_id = "1642E726B682B518!72464"
        self.chunk_size = 10 * 1024 * 1024
    
    def refresh_access_token(self):
        self.access_token = self.auth.get_fixed_access_token()
        with open(f"{self.absolut_path}/token.key", "w+") as f:
            f.write(self.access_token)
        
    def create_folder(self, folder_name, dad_folder_id=None):
        folder_name = self.utils.clean_folder_name(folder_name)
        
        print(folder_name)
        if dad_folder_id == None:
            dad_folder_id = self.filmes_folder_id
            
        url = f'https://graph.microsoft.com/v1.0/me/drive/items/{dad_folder_id}/children'
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

        data = {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }

        req = requests.post(url, headers=headers, json=data)
        
        data = req.json()
        
        print(data)
        
        if "error" in data:
            if data["error"]["code"] == "InvalidAuthenticationToken":
                self.refresh_access_token()
                return self.create_folder(folder_name)
        
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
    
    def _create_upload_session(self, folder_id, file_name):
        url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}:/{file_name}:/createUploadSession"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        req = requests.post(url, headers=headers)
        
        data = req.json()
        
        if "error" in data:
            if data["error"]["code"] == "InvalidAuthenticationToken":
                self.refresh_access_token()
                return self._create_upload_session(folder_id, file_name)
        
        return data["uploadUrl"]
    
    def list_files(self, folder_id):
        url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        req = requests.get(url, headers=headers)
        
        data = req.json()
        
        if "error" in data:
            if data["error"]["code"] == "InvalidAuthenticationToken":
                self.refresh_access_token()
                return self.list_files(folder_id)
        
        return data
    
    def get_m3u8_file_id(self, folder_id):
        files = self.list_files(folder_id)
        
        for file in files["value"]:
            if file["name"] == "output.m3u8":
                return str(file["id"])
        
        return False

    def get_file_id(self, folder_id, file_name):
        files = self.list_files(folder_id)
        
        for file in files["value"]:
            if file["name"] == file_name:
                return str(file["id"])
        
        return False
        
    
    def upload_file(self, folder_id, file_path):
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        upload_url = self._create_upload_session(folder_id, file_name)

        headers = {"Authorization": f"Bearer {self.access_token}"}
        with open(file_path, "rb") as file:
            chunk_start = 0
            while chunk_start < file_size:
                chunk_end = min(chunk_start + self.chunk_size, file_size) - 1
                chunk_length = chunk_end - chunk_start + 1

                file.seek(chunk_start)
                chunk_data = file.read(chunk_length)

                headers.update({
                    "Content-Length": str(chunk_length),
                    "Content-Range": f"bytes {chunk_start}-{chunk_end}/{file_size}"
                })

                req = requests.put(upload_url, headers=headers, data=chunk_data)
                
                data = req.json()
                
                if "error" in data:
                    if data["error"]["code"] == "InvalidAuthenticationToken":
                        self.refresh_access_token()
                        return self.upload_file(folder_id, file_path)
                
                if req.status_code not in [200, 201, 202]:
                    print(f"Erro no upload: {data}")
                    break

                chunk_start += chunk_length
                print(f"Chunk {chunk_start}/{file_size} enviado")

        print("Upload concluído!")
    
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
    #print(starter.get_downloads_frames_links(starter.filmes_folder_id))
    id = starter.get_m3u8_file_id("1642E726B682B518!166366")
    print(id)
    #starter.upload_file(starter.filmes_folder_id, "phonk.webm")