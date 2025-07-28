# 🎞️🤖 Site Com Filmes Cristãos Script

> Um Script Python que prepara e sobe filmes, faixas de áudio, legenda e querys no MySQL dos filmes do Site de Filmes Cristãos.

![Python](https://img.shields.io/badge/Python-8.2+-356e9f?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-00758f?style=for-the-badge&logo=MySQL&logoColor=white)
![License](https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge)

## 🎥 Funcionamento do projeto

Para entender melhor o funcionamento do projeto com vídeos demonstrativos, imagens, e toda a história de desenvolvimento, acompanhe a matéria completa no meu site portfólio: 

**Link da Matéria Completa:** [https://phgodoycosta.com.br/projeto/site-com-filmes](https://phgodoycosta.com.br/projeto/site-com-filmes)

## 📦 Instalação

```bash
# Clonar o repositório
$ git clone https://github.com/PHGodoyCosta/Site-de-filmes-script
cd Site-de-filmes-script

# Instalar dependências Python
$ pip3 install -r ./requirements.txt

# Configurar variáveis de ambiente
$ cp .env.example .env

# Crie sua função para Autenticação One Drive
$ cp auth.example.py auth.py

# Inicie o upload e tratamento do filme com:
$ python3 main.py
```

## ⚙️ Configuração

Configure as seguintes variáveis no arquivo `.env`:

```env
# Adicionar suas variáveis para acesso ao banco de dados

DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=site_com_filmes_db
DB_USERNAME=
DB_PASSWORD=
```
Não esqueça de criar o arquivo `auth.py` retornando seu Token do One Drive:

```py
class Auth:
    def get_fixed_access_token():
        return "<O Token de Acesso do seu One drive>"
```