#Carrega as variáveis salvas no arquivo oculto .env
import os
from dotenv import load_dotenv

# diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

# carrega as informações do .env
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bf6e297f3715d145529fcd9d4783a7b7'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    API_URL = 'https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent'


# essa linha é para facilitar a importação da chave de dentro da classe Config para o nosso arquivo app/agent.py 
GEMINI_API_KEY = Config.GEMINI_API_KEY

# verificação de segurança para garantir que a chave foi carregada 
if not GEMINI_API_KEY:
    raise ValueError("ERRO: A variável GEMINI_API_KEY não foi encontrada no arquivo .env. Verifique se o arquivo existe e se a sua chave está lá dentro!")