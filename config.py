import os
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()

# Caminho do modelo GGUF do deepseek
MODEL_PATH = os.getenv("MODEL_PATH")

# Configurações do PostgreSQL
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}
