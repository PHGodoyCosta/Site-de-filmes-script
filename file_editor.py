import os
import ffmpeg
from datetime import timedelta
from moviepy import VideoFileClip
from one_drive import One_Drive
import av
import subprocess

class Editor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.movie_name = self.file_name.split(".")[0]
        self.file_path = f"{os.getcwd()}/{self.file_name}"
        self.absolut_path = os.path.dirname(os.path.abspath(__file__))
        self.one_drive = One_Drive()
    
    def _extrair_audio(self, faixa_index, output_file, type="copy"):
        if type == "copy":
            try:
                ffmpeg.input(self.file_path).output(output_file, codec='copy', map=f'0:a:{faixa_index}').run()
            except ffmpeg.Error as e:
                print("Erro FFMPEG")
                print(e)
        
    def _extract_audios(self, faixas, folder_id):
        for i in range(0, len(faixas)):
            faixa = faixas[i]
            folder_name = f"Faixa_{i}"
            file_name = f"{folder_name}.{faixa['codec']}"
            file_path = f"{self.absolut_path}/{folder_name}/{file_name}"
            
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
            os.chdir(folder_name)
            one_drive_folder = self.one_drive.create_folder(folder_name, folder_id)
            
            self._extrair_audio(i, file_name)
            self.cutting_files(file_path, one_drive_folder, type="audio")

            os.chdir("..")
    
    def _extract_legenda(self, file_name, index):
        try:
            #ffmpeg.input(file_path, si=index).output(file_name).run()
            #ffmpeg.input(file_path, map=f"0:s:{index}").output(file_name).run()
            ffmpeg.input(self.file_path).output(file_name, map=f"0:s:{index}").run()
            print(f"Legenda extraída e salva!")
        except ffmpeg.Error as e:
            print(f"Erro ao extrair legenda!")
            raise Exception(e)
    
    def _extract_legendas(self, subtitles, folder_id):
        for i in range(0, len(subtitles) - 1):
            subtitle = subtitles[i]
            if subtitle["language"] == "und":
                file_name = f"legenda_{i}.srt"
            else:
                file_name = f"legenda_{subtitle['language']}.srt"
            #file_path = f"{self.absolut_path}/legendas/{file_name}"
            
            if not os.path.isdir("legendas"):
                os.mkdir("legendas")
            os.chdir("legendas")
            
            self._extract_legenda(file_name, i)
            self.one_drive.upload_file(folder_id, file_name)
            
            os.chdir(self.absolut_path)
    
    def check_file_length(self, file_path):
        byte_size = os.path.getsize(file_path)
        mb_size = int((byte_size / 1064) / 1064)
        
        if (mb_size < 30):
            return True
        return False
    
    def _format_hour_number(self, number):
        if number < 10:
            return f"0{number}"
        return str(number)
    
    def get_movie_duration(self, file_path):
        try:
            probe = ffmpeg.probe(file_path)
            duration = int(float(probe['format']['duration']))
        except ffmpeg.Error as e:
            print("Erro ao obter duração!")
            raise Exception(e)
        
        return timedelta(seconds=duration)
    
    def get_audio_duration(self, file_path):
        try:
            probe = ffmpeg.probe(file_path, v='error', select_streams='a', show_entries='stream=duration')
            duration = int(float(probe['streams'][0]['duration']))
        except ffmpeg.Error as e:
            print(f"Erro ao obter a duração do áudio: {e}")
            return None
        
        return timedelta(seconds=duration)
    
    def remux_video(self, file_path, name_file):
        try:
            ffmpeg.input(file_path).output(name_file, c='copy').run(overwrite_output=True)
            
            #Compress
            ffmpeg.input(file_path).output(f"{name_file.replace('.mp4', '')}_compress.mp4", vf="scale=1280:720", video_bitrate="500k", audio_bitrate="128k", vcodec="libx265", acodec="aac", ar="44100", ac="2", crf=28).run(overwrite_output=True)
        except ffmpeg.Error as e:
            print(f"Erro ao remuxar {file_path}")
            raise Exception(e)
    
    def cut_movie_file_subprocess(self, file_path, name_file, start, end):
        if start == timedelta(seconds=0):
            print("Primeiro Clipe")
            try:
                # Monta o comando FFmpeg para o caso de start == 0
                command = [
                    'ffmpeg',
                    '-i', file_path,  # Arquivo de entrada
                    '-t', str(end.total_seconds()),  # Tempo de corte (final)
                    '-c', 'copy',  # Copiar codec sem reencodar
                    '-reset_timestamps', '1',  # Resetar timestamps
                    name_file  # Arquivo de saída
                ]
                # Executa o comando
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Erro ao cortar o arquivo {name_file}")
                raise Exception(e)
        else:
            print("Outros Clipes")
            try:
                # Monta o comando FFmpeg para o caso de start > 0
                command = [
                    'ffmpeg',
                    '-i', file_path,  # Arquivo de entrada
                    '-ss', str(start.total_seconds()),  # Tempo de início do corte
                    '-t', str(end.total_seconds()),  # Tempo de corte (final)
                    '-c', 'copy',  # Copiar codec sem reencodar
                    '-reset_timestamps', '1',  # Resetar timestamps
                    name_file  # Arquivo de saída
                ]
                # Executa o comando
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Erro ao cortar o arquivo {name_file}")
                raise Exception(e)

    def cut_movie_file(self, file_path, name_file, start, end):
        if start == timedelta(seconds=0):
            print("Primeiro Clipe")
            try:
                ffmpeg.input(file_path).output(name_file, t=end.total_seconds(), c='copy', reset_timestamps=1).run()
            except ffmpeg.Error as e:
                print(f"Erro ao cortar o arquivo {name_file}")
                raise Exception(e)
        else:
            print("Outros Clipes")
            try:
                ffmpeg.input(file_path, ss=start.total_seconds()).output(name_file, t=end.total_seconds(), c='copy', reset_timestamps=1).run()
            except ffmpeg.Error as e:
                print(f"Erro ao cortar o arquivo {name_file}")
                raise Exception(e)
    
    def cut_audio_file(self, file_path, name_file, start, end):
        command = [
            'ffmpeg', 
            '-i', file_path,
            '-ss', str(start),
            '-to', str(end),
            '-c:a', 'aac',
            '-b:a', '256k',
            '-ar', '44100',
            name_file
        ]
        
        try:
            subprocess.run(command, check=True)
            print(f"Arquivo cortado com sucesso: {name_file}")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao cortar o arquivo: {e}")
    
    def cutting_files(self, file_path, folder_id, type="movie"):
        if type == "movie":
            duration = self.get_movie_duration(file_path)
        elif type == "audio":
            duration = self.get_audio_duration(file_path)
        cut_duration = timedelta(seconds=0)
        extension_file = file_path.split(".")[len(file_path.split(".")) - 1]
        counter = 0
        
        while cut_duration < duration:
            if cut_duration + timedelta(minutes=1) < duration:
                cut_time = timedelta(minutes=1)
            else:
                cut_time = duration - cut_duration
            
            #print(f"START: {cut_duration} - END: {cut_time}")
            #self.cut_movie_file(file_path, f"{counter}.{extension_file}", start=cut_duration, end=cut_time)
            #self.remux_video(f"{counter}.{extension_file}", f"{counter}_remux.{extension_file}")
            #self.cut_movie_file_moviepy(file_path, f"{counter}.{extension_file}", start=cut_duration, end=cut_time)
            #self.cut_movie_file_av(file_path, f"{counter}.{extension_file}", start=cut_duration, end=cut_time)
            if type == "audio":
                file_name = f"{counter}.m4a"
                self.cut_audio_file(file_path, file_name, start=cut_duration, end=(cut_time + cut_duration))
            else:
                file_name = f"{counter}.{extension_file}"
                self.cut_movie_file_subprocess(file_path, file_name, start=cut_duration, end=cut_time)
                if not self.check_file_length(file_name):
                    print("ALERTA! CORTES GRANDES")
                    print("Verificar os próximos")
                    input("> ")
            self.one_drive.upload_file(folder_id, file_name)
            
            counter += 1
            cut_duration += cut_time
    
    def temp(self):
        os.chdir("filme")
        #faixa = f"{os.getcwd()}/Faixa_0.ac3"
        
        #print(self.get_audio_duration(faixa))
        #self.cutting_files(f"{self.absolut_path}/filme/filme.mp4")
        self.cutting_files(self.file_path)
        
    
    def _extract_movie_video(self):
        if not os.path.isdir("Filme_Video"):
            os.mkdir("Filme_Video")
        os.chdir("Filme_Video")
        
        try:
            ffmpeg.input(self.file_path).output(self.file_name, an=None, c='copy').run()
        except ffmpeg.Error as e:
            print("Erro ao executar ffmpeg:")
            raise Exception(e)
        
        os.chdir("..")
        
    def _list_audios_in_file(self):
        probe = ffmpeg.probe(self.file_path, v='error', select_streams='a', show_entries='stream=index,codec_name,codec_type,language')
    
        faixas = []
        
        for stream in probe['streams']:
            faixas.append({
                'index': stream['index'],
                'codec': stream['codec_name'],
                'codec_type': stream['codec_type'],
                'language': stream.get('language', 'Unknown')
            })
        
        return faixas
    
    def _list_subtitles_in_file(self):
        try:
            probe = ffmpeg.probe(self.file_path, v='error', select_streams='s', show_entries='stream=index,codec_name,codec_type')
            
            subtitles = []
            
            for stream in probe['streams']:
                if stream['codec_type'] == 'subtitle':
                    subtitles.append({
                        'index': stream['index'],
                        'codec': stream['codec_name'],
                        'type': stream['codec_type'],
                        'language': stream["tags"]["language"]
                    })
            
            return subtitles
        except ffmpeg.Error as e:
            print("Erro ao tentar acessar o arquivo:", e)
            raise Exception(e)
    
    
if __name__ == "__main__":
    starter = Editor("filme2.mkv")
    #starter.temp()
    #starter.cut_movie_file(starter.file_path, "corte_teste.mp4", start=timedelta(minutes=1), end=timedelta(minutes=1))
    # duration = starter.get_movie_duration(starter.file_path)
    # print(duration)
    #starter._extract_movie_video()
    
    legendas = starter._list_subtitles_in_file()
    print(legendas)
    # starter._extract_legendas(legendas)
    
    # audios = starter._list_audios_in_file()
    # print(audios)
    #starter._extract_audios(audios)