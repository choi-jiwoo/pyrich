from collections.abc import Iterable
import psycopg2
from urllib.parse import urlparse


class PostgreSQL:

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self._parse_database_url()
        self._connect()

    def _parse_database_url(self) -> None:
        connection_info = urlparse(self.database_url)
        self.dbname = connection_info.path.lstrip('/')
        self.user = connection_info.username
        self.password = connection_info.password
        self.host = connection_info.hostname
        self.port = connection_info.port

    def _connect(self) -> None:
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError:
            raise

    def run_query(self, query: str, values: Iterable = None) -> None:
        try:
            self.cur.execute(query, values)
        except psycopg2.ProgrammingError:
            raise

        except Exception as e:
            print(e)

    def show_table(self, table: str) -> None:
        try:
            query = f'SELECT * FROM {table};'
            self.run_query(query)
            result = self.cur.fetchall()
            for item in result:
                print(item)
        except Exception as e:
            print(e)

    def __del__(self) -> None:
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def __repr__(self) -> str:
        return f"PostgreSQL(database_url='{self.database_url}')"