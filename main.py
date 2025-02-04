from one_drive import One_Drive
from file_editor import Editor
from db import DB
import json
import os

class Main:
    def __init__(self, tempMode=False):
        self.absolut_path = os.path.dirname(os.path.abspath(__file__))
        self.preload = json.loads(open(f"{self.absolut_path}/preload.json", "r+").read())
        self.file_name = self.preload["name"]
        
        if os.path.isabs(self.preload["local"]):
            self.file_path = self.preload["local"]
        else:
            self.file_path = os.path.abspath(self.file_name)
        self.file_extension = self.file_path.split(".")[len(self.file_path.split(".")) - 1]
        self.one_drive = One_Drive()
        self.db = DB()
        # print(self.file_name)
        # print(self.file_path)
        # print(self.file_extension)
        self.editor = Editor(self.file_name, self.file_path, self.file_extension)
        if not tempMode:
            self.main_folder_id = self.one_drive.create_folder(self.preload["name"] if self.preload["name"] else self.movie["name"], self.one_drive.filmes_folder_id)
    
    # def temp(self):
    #     self.editor.cutting_files(file)
    
    def extract_and_cut_audios(self, filme_hash):
        audios_folder_id = self.one_drive.create_folder("Audios", self.main_folder_id)
        audios = self.editor._list_audios_in_file()
        print(audios)
        folder_id = self.editor._extract_audios(audios, audios_folder_id)
        
        m38u_id = self.one_drive.get_m3u8_file_id(folder_id)
        filme_db = self.db.get_filme_by_hash(filme_hash)[0]
        return self.db.insert_audio(folder_id, m38u_id, filme_db[0])
    
    def extract_legendas(self):
        subtitles_folder_id = self.one_drive.create_folder("Legendas", self.main_folder_id)
        subtitles = self.editor._list_subtitles_in_file()
        print(subtitles)
        self.editor._extract_legendas(subtitles, subtitles_folder_id)
    
    def extract_video(self):
        videos_folder_id = self.one_drive.create_folder("Videos", self.main_folder_id)
        self.editor._extract_movie_video()
        
        os.chdir("Filme_Video")
        self.editor.cutting_files(f"filme.{self.file_extension}", videos_folder_id)
        os.chdir("..")
        
        m38u_id = self.one_drive.get_m3u8_file_id(videos_folder_id)
        return self.db.insert_filme(self.preload["name"], videos_folder_id, m38u_id)
    
    def main(self):
        self.extract_legendas()
        filme_hash = self.extract_video()
        self.extract_and_cut_audios(filme_hash)
        #self.editor
    
    def temp(self):
        #audios = self.editor._list_audios_in_file()
        #print(audios)
        #self.editor._extrair_audio(0, "testing_function.aac")
        self.editor.cutting_files(f"{self.editor.absolut_path}/Faixa_0/testing_function.aac", "one_drive_folder", type="audio")
        
if __name__ == "__main__":
    starter = Main(tempMode=False)
    starter.main()
    #starter.temp()
    
    