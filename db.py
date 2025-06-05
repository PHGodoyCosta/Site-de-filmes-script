import mysql.connector
from dotenv import load_dotenv
import os
from uuid import uuid4

class DB:
    def __init__(self):
        load_dotenv()
        self.absolut_path = os.path.dirname(os.path.abspath(__file__))
        self.con = 0
        self.log("-- Inserindo outro filme...")
        
        
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

    def log(self, content):
        with open(f"{self.absolut_path}/log.sql", "a+") as f:
            f.write(f"\n\n{content}")

    def get_filme_by_hash(self, hash):
        self.get_con()
        self.cursor.execute(f"SELECT * FROM filmes WHERE hash = '{hash}';")
        
        data = self.cursor.fetchall()
        self.close()
        
        return data
    
    def get_audio_by_hash(self, hash):
        self.get_con()
        self.cursor.execute(f"SELECT * FROM audios WHERE hash = '{hash}';")
        data = self.cursor.fetchall()
        self.close()
        
        return data
    
    def insert_filme(self, name, folder_id, hls_id, poster, backdrop, year="NULL", categories="NULL", runtime="NULL", description="NULL"):
        
        self.get_con()
        hash = uuid4()
        
        command = f'INSERT INTO filmes (hash, name, folder_id, hls_id, poster, backdrop, year, categories, duration, description) VALUES ("{hash}", "{name}", "{folder_id}", "{hls_id}", "{poster}", "{backdrop}", "{year}", "{categories}", "{runtime}", "{description}");'.replace('"NULL"', 'NULL')
        self.cursor.execute(command)
        
        self.con.commit()
        self.log(command)
        self.close()
        
        return hash
    
    def insert_audio(self, folder_id, hls_id, filme_id, name=None):
        hash = uuid4()
        self.get_con()
        
        if name:
            command = f'INSERT INTO audios (hash, name, folder_id, hls_id, filme_id) VALUES ("{hash}", "{name}", "{folder_id}", "{hls_id}", {int(filme_id)});'
        else:
            command = f'INSERT INTO audios (hash, folder_id, hls_id, filme_id) VALUES ("{hash}", "{folder_id}", "{hls_id}", {int(filme_id)});'
        
        self.cursor.execute(command)
        
        self.con.commit()
        self.log(command)
        self.close()
        
        return hash

    def insert_legenda(self, folder_id, file_id, filme_id, name=None, isForced=False):
        hash = uuid4()
        self.get_con()
        
        command = f'INSERT INTO legendas(hash, name, folder_id, file_id, isForced, filme_id) VALUES ("{hash}", "{name if name else "NULL"}", "{folder_id}", "{file_id}", {1 if isForced else 0}, "{filme_id}");'
        #self.cursor.execute(command)
        
        #self.con.commit()
        self.log(command)
        self.close()
        
        return hash
    
    def close(self):
        return self.con.close()
    
if __name__ == "__main__":
    starter = DB()
    starter.insert_legenda("1642E726B682B518!167205", "1642E726B682B518!167219", 3, name="Legenda Teste")