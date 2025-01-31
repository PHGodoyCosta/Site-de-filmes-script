from one_drive import One_Drive
from file_editor import Editor
import os

class Main:
    def __init__(self, file_name):
        self.file_name = file_name
        self.movie_name = self.file_name.split(".")[0]
        self.file_path = f"{os.getcwd()}/{self.file_name}"
        self.one_drive = One_Drive()
        self.editor = Editor(self.file_name)
        self.main_folder_id = self.one_drive.create_folder(self.file_name, self.one_drive.filmes_folder_id)
    
    # def temp(self):
    #     self.editor.cutting_files(file)
    
    def extract_and_cut_audios(self):
        audios_folder_id = self.one_drive.create_folder("Audios", self.main_folder_id)
        audios = self.editor._list_audios_in_file()
        print(audios)
        self.editor._extract_audios(audios, audios_folder_id)
    
    def extract_legendas(self):
        subtitles_folder_id = self.one_drive.create_folder("Legendas", self.main_folder_id)
        subtitles = self.editor._list_subtitles_in_file()
        print(subtitles)
        self.editor._extract_legendas(subtitles, subtitles_folder_id)
    
    def extract_video(self):
        videos_folder_id = self.one_drive.create_folder("Videos", self.main_folder_id)
        self.editor._extract_movie_video()
        
        os.chdir("Filme_Video")
        self.editor.cutting_files(self.editor.file_path, videos_folder_id)
        os.chdir("..")
    
    def main(self):
        self.extract_legendas()
        self.extract_video()
        self.extract_and_cut_audios()
        #self.editor
    
if __name__ == "__main__":
    starter = Main("filme2.mkv")
    starter.main()
    