from one_drive import One_Drive
from file_editor import Editor

class Main:
    def __init__(self, file_path):
        self.file_path = file_path
        self.one_drive = One_Drive()
        self.editor = Editor(self.file_path)
    
    # def temp(self):
    #     self.editor.cutting_files(file)
    
    def extract_and_cut_audios(self):
        audios = starter._list_audios_in_file()
        print(audios)
        starter._extract_audios(audios)
    
if __name__ == "__main__":
    starter = Main()
    starter.temp()