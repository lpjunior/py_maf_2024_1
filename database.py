import sqlite3


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conectado no {db_file} SQLite database")
    except sqlite3.Error as e:
        print(f"Erro ao criar a conexão com o banco de dados {e}")
    return conn


def create_table(conn):
    try:
        sql_create_table_sql = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        nome text NOT NULL,
                                        idade integer NOT NULL
                                    ); """
        c = conn.cursor()
        c.execute(sql_create_table_sql)
        print("Tabela criada com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela {e}")


def insert_user(conn, user):
    sql = ''' INSERT INTO users(nome,idade)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid


def select_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for row in rows:
        print(row)


def update_user(conn, user):
    sql = ''' UPDATE users
              SET nome = ?,
                  idade = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()


def delete_user(conn, id):
    sql = 'DELETE FROM users WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def main():
    database = r"users.db"
    conn = create_connection(database)
    with conn:
        create_table(conn)
        user = ('João', 20)
        insert_user(conn, user)
        select_all_users(conn)
        user = ('Maria', 25, 1)
        update_user(conn, user)
        select_all_users(conn)
        delete_user(conn, 1)
        select_all_users(conn)


if __name__ == '__main__':
    main()
