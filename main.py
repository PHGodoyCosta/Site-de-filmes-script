from one_drive import One_Drive
from editor import Editor

class Main:
    def __init__(self, file_path):
        self.file_path = file_path
        self.one_drive = One_Drive()
        self.editor = Editor(self.file_path)