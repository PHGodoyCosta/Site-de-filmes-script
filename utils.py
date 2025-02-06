import json
import subprocess
import re
import os

class Utils:
    def __init__(self):
        self.absolut_path = os.path.dirname(os.path.abspath(__file__))
    
    def get_preload_variables(self):
        file = open(f"preload.json", "r+").read()
        
        return json.loads(file)


    def get_faixa_audio(self, editor):
        faixas = editor._list_audios_in_file()
        print(faixas)
        
        for i in range(0, len(faixas)):
            if i == 1:
                faixa = faixas[i]
                folder_name = f"Faixa_{i}"
                file_name = f"{folder_name}.aac"
                
                editor._extrair_audio(i, file_name)
        #self.editor._extrair_audio(0, "testing_function.aac")
        #self.editor.cutting_files(f"{self.editor.absolut_path}/Faixa_0/testing_function.aac", "one_drive_folder", type="audio")

    def conversor_srt_to_vvt(self, file_path):
        path = f'{self.absolut_path}/Legendas'
        command = [
            'srt-vtt',
            file_path,
            '-o', path
        ]

        try:
            subprocess.run(command, check=True)
        except Exception as e:
            print(f"Erro ao Converter SRT TO VTT: {e}")
            raise Exception(e)
        else:
            os.chdir(path)
            
            file_name = str(file_path).split("/")
            file_name = file_name[len(file_name) - 1]
            file_name = file_name.replace(".srt", ".vtt")
            #os.rename(file_name, "legenda.vtt")
            os.chdir("..")
        
        return f"{path}/{file_name}"
    
    def editing_vtt_file(self, file_name):
        linhas = open(file_name, "r+").readlines()
        
        novo_conteudo = []
        for i, linha in enumerate(linhas):
            
            match = re.search(r"(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3})", linha)
            if match:
                linha = match.group(1).strip() + " line:85%\n"  # Adiciona a linha no final do tempo

            novo_conteudo.append(linha)

        with open(file_name, 'w+', encoding='utf-8') as f:
            f.writelines(novo_conteudo)
    
    def format_categories_movie_db(self, categories):
        gen = []
        for categorie in categories:
            gen.append(categorie["name"])
            
        return ", ".join(gen)
    
    def format_runtime_movie_db(self, runtime):
        if runtime < 60:
            return f"{runtime} m"
        
        return f"{int(runtime / 60)}h {int(runtime % 60)}m"


if __name__ == "__main__":
    starter = Utils()
    c = starter.format_categories([
		{
			"id": 18,
			"name": "Drama"
		},
        {
            "id": 20,
            "name": "Ação"
        },
        {
            "id": 21,
            "name": "Comedia"
        }
	])
    print(c)
    #starter.editing_vtt_file("legenda.vtt")
    #starter.conversor_srt_to_vvt("/home/phgodoycosta/Downloads/torrents/Cruzada 2005 [1080p] WWW.BLUDV.COM/legenda.vtt")