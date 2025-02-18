import psycopg2
from config import DB_CONFIG

def connect_db():
    """Cria conexão com o baco de dados PostgresSQL."""
    return psycopg2.connect(**DB_CONFIG)

def query_db(query):
    """Executa uma consulta SQL e retorna os resultados"""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
