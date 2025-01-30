import os
import ffmpeg
from datetime import timedelta

class Editor:
    def __init__(self, file_name):
        self.file_name = file_name
        self.movie_name = self.file_name.split(".")[0]
        self.file_path = f"{os.getcwd()}/{self.file_name}"
    
    def _extrair_audio(self, faixa_index, output_file, type="copy"):
        if type == "copy":
            try:
                ffmpeg.input(self.file_path).output(output_file, codec='copy', map=f'0:a:{faixa_index}').run()
            except ffmpeg.Error as e:
                print("Erro FFMPEG")
                print(e)
        
    def _extract_audios(self, faixas):
        for i in range(0, len(faixas)):
            faixa = faixas[i]
            audio_name = f"Faixa_{i}"
            
            if not os.path.isdir(audio_name):
                os.mkdir(audio_name)
            os.chdir(audio_name)
            
            self._extrair_audio(i, f"{audio_name}.{faixa['codec']}")

            os.chdir("..")
    
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
        
        # total_min = int(duration / 60)
        # hours = int(total_min / 60)
        # min = total_min - (hours * 60)
        # sec = duration - ((min * 60) + (hours * 60 * 60))
        
        return timedelta(seconds=duration)

    def cut_movie_file(self, file_path, name_file, start="0:00:0", end="0:00:0"):
        if start == "0:00:0":
            try:
                ffmpeg.input(file_path).output(name_file, t=end, c='copy').run()
            except ffmpeg.Error as e:
                print(f"Erro ao cortar o arquivo {name_file}")
                raise Exception(e)
        else:
            try:
                ffmpeg.input(file_path, ss=start).output(name_file, t=end, c='copy').run()
            except ffmpeg.Error as e:
                print(f"Erro ao cortar o arquivo {name_file}")
                raise Exception(e)
    
    def cutting_files(self, file_path)
            
    
    def _extract_movie_video(self):
        if not os.path.isdir(self.movie_name):
            os.mkdir(self.movie_name)
        os.chdir(self.movie_name)
        
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
    
    
if __name__ == "__main__":
    starter = Editor("filme.mp4")
    duration = starter.get_movie_duration(starter.file_path)
    print(duration)
    #starter._extract_movie_video()
    # audios = starter._list_audios_in_file()
    # print(audios)
    # starter._extract_audios(audios)