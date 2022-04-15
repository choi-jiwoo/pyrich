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
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self.cur = self.conn.cursor()

    def __del__(self) -> None:
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def __repr__(self) -> str:
        return f"PostgreSQL(database_url='{self.database_url}')"