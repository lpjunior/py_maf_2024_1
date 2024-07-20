from django.core.management.base import BaseCommand
from contatos.db_manager import connect_to_db, fetch_data, close_connection


class Command(BaseCommand):
    help = 'Fetches data from PostgreSQL database'

    def handle(self, *args, **kwargs):
        conn = connect_to_db()
        if conn:
            query = "SELECT * FROM usuario;"
            results = fetch_data(conn, query)
            for row in results:
                self.stdout.write(str(row))
            close_connection(conn)
