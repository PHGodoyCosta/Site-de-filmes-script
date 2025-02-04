import mysql.connector
from dotenv import load_dotenv
import os
from uuid import uuid4

class DB:
    def __init__(self):
        load_dotenv()
        self.con = self.get_con()
        
    def get_con(self):
        self.con = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USERNAME"),
            port=os.getenv("DB_PORT"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE")
        )
        
        self.cursor = self.con.cursor()
        
        return self.con

    def get_filme_by_hash(self, hash):
        self.cursor.execute(f"SELECT * FROM filmes WHERE hash = '{hash}';")
        
        return self.cursor.fetchall()
    
    def get_audio_by_hash(self, hash):
        self.cursor.execute(f"SELECT * FROM audios WHERE hash = '{hash}';")
        
        return self.cursor.fetchall()
    
    def insert_filme(self, name, folder_id, hls_id, poster, backdrop):
        hash = uuid4()
        
        self.cursor.execute(f'INSERT INTO filmes (hash, name, folder_id, hls_id, poster, backdrop) VALUES ("{hash}", "{name}", "{folder_id}", "{hls_id}", "{poster}", "{backdrop}");')
        
        self.con.commit()
        
        return hash
    
    def insert_audio(self, folder_id, hls_id, filme_id, name=None):
        hash = uuid4()
        
        if name:
            self.cursor.execute(f'INSERT INTO audios (hash, name, folder_id, hls_id, filme_id) VALUES ("{hash}", "{name}", "{folder_id}", "{hls_id}", {int(filme_id)});')
        else:
            self.cursor.execute(f'INSERT INTO audios (hash, folder_id, hls_id, filme_id) VALUES ("{hash}", "{folder_id}", "{hls_id}", {int(filme_id)});')
        
        self.con.commit()
        
        return hash
    
    def close(self):
        return self.con.close()
    
if __name__ == "__main__":
    starter = DB()
    starter.simple_get()