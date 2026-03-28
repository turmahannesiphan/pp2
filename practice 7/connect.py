import psycopg2
from config import params

def get_connection():
    """Создает и возвращает объект соединения с БД"""
    return psycopg2.connect(**params)