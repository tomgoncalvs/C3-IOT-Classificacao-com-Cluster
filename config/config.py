from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do .env
load_dotenv()

# Configurações para conexão ao banco de dados Oracle
ORACLE_HOST = os.getenv("ORACLE_HOST")
ORACLE_PORT = os.getenv("ORACLE_PORT")
ORACLE_SERVICE_NAME = os.getenv("ORACLE_SERVICE_NAME")
ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")

# Chave da API do OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
