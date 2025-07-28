from one_drive import One_Drive
from file_editor import Editor
from db import DB
from moviedb import MovieDB
from utils import Utils
import json
import os
import shutil

class Main:
    def __init__(self, tempMode=False):
        self.absolut_path = os.path.dirname(os.path.abspath(__file__))
        self.preload = json.loads(
            open(f"{self.absolut_path}/preload.json", "r+").read())
        self.moviedb = MovieDB()
        self.file_name, self.backdrop, self.poster, self.description, self.year, self.categories, self.runtime = self.moviedb.find_movie_by_id(
            self.preload["movieId"])
        # self.file_name = self.preload["name"]

        if os.path.isabs(self.preload["local"]):
            self.file_path = self.preload["local"]
        else:
            self.file_path = os.path.abspath(self.file_name)
        self.file_extension = self.file_path.split(
            ".")[len(self.file_path.split(".")) - 1]
        self.one_drive = One_Drive()
        self.db = DB()
        self.utils = Utils()
        self.editor = Editor(
            self.file_name, self.file_path, self.file_extension)
        if not tempMode:
            self.main_folder_id = self.one_drive.create_folder(
                self.file_name, self.one_drive.filmes_folder_id)
        else:
            self.main_folder_id = "1642E726B682B518!169249"

    def extract_and_cut_audios(self, filme_hash):
        audios_folder_id = self.one_drive.create_folder(
            "Audios", self.main_folder_id)
        audios = self.editor._list_audios_in_file()
        print(audios)
        folders_id = self.editor._extract_audios(audios, audios_folder_id)

        for folder_id in folders_id:
            m38u_id = self.one_drive.get_m3u8_file_id(folder_id)
            filme_db = self.db.get_filme_by_hash(filme_hash)[0]
            self.db.insert_audio(folder_id, m38u_id, filme_db[0])

    def extract_legendas(self, filme_hash):
        legendas_ids = []
        subtitles_folder_id = None

        # Legendas escolhidas em preload
        if self.preload.get("legendas"):
            if not os.path.isdir("Legendas"):
                os.mkdir("Legendas")
            os.chdir("Legendas")
            subtitles_folder_id = self.one_drive.create_folder(
                "Legendas", self.main_folder_id)
            for legenda in self.preload["legendas"]:
                ex_file_name = legenda["local"].split(
                    "/")[len(legenda["local"].split("/")) - 1]
                extension = ex_file_name.split(
                    ".")[len(ex_file_name.split(".")) - 1]
                if extension == "srt":
                    legenda_path = self.utils.conversor_srt_to_vvt(
                        legenda["local"])
                elif extension == "vtt":
                    legenda_path = f"{self.absolut_path}/Legendas/legenda.vtt"
                    shutil.move(legenda["local"], legenda_path)

                self.utils.editing_vtt_file(legenda_path)
                self.one_drive.upload_file(subtitles_folder_id, legenda_path)
                file_name = legenda_path.split(
                    "/")[len(legenda_path.split("/")) - 1]
                legenda_id = self.one_drive.get_file_id(
                    subtitles_folder_id, file_name)
                filme_db = self.db.get_filme_by_hash(filme_hash)[0]
                self.db.insert_legenda(
                    subtitles_folder_id, legenda_id, filme_db[0])
                legendas_ids.append(legenda_id)
            os.chdir("..")

        # Legendas do arquivo de vídeo

        subtitles = self.editor._list_subtitles_in_file()
        print(f"\n\nAchei isso: {subtitles}")
        if subtitles:
            if not subtitles_folder_id:
                subtitles_folder_id = self.one_drive.create_folder(
                    "Legendas", self.main_folder_id)

            self.editor._extract_legendas(
                subtitles, subtitles_folder_id, filme_hash)

    def extract_video(self):
        videos_folder_id = self.one_drive.create_folder(
            "Videos", self.main_folder_id)
        self.editor._extract_movie_video()

        os.chdir("Filme_Video")
        self.editor.cutting_files(
            f"filme.{self.file_extension}", videos_folder_id)
        os.chdir("..")

        m38u_id = self.one_drive.get_m3u8_file_id(videos_folder_id)

        return self.db.insert_filme(self.file_name, videos_folder_id, m38u_id, self.poster, self.backdrop, year=self.year, categories=self.categories, runtime=self.runtime, description=self.description)

    def main(self):
        filme_hash = self.extract_video()
        print(f"Filme HASH -> {filme_hash}")
        self.extract_and_cut_audios(filme_hash)
        self.extract_legendas(filme_hash)


if __name__ == "__main__":
    starter = Main(tempMode=False)
    starter.main()
    
