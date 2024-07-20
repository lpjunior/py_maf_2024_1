import psycopg2
import os


def connect_to_db():
    try:
        # Conectar ao banco de dados PostgreSQL usando as variáveis de ambiente
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def fetch_data(conn, query):
    try:
        # Executar a consulta SQL e buscar os dados
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return []


def close_connection(conn):
    try:
        # Fechar a conexão com o banco de dados
        conn.close()
    except Exception as e:
        print(f"Erro ao fechar a conexão com o banco de dados: {e}")
