from collections.abc import Iterable
import os
import pandas as pd
import psycopg2
from urllib.parse import urlparse


class PostgreSQL:

    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        self._parse_database_url()
        self._connect()
        self._create_transaction_table()

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

    def _create_transaction_table(self) -> None:
        query = ('CREATE TABLE IF NOT EXISTS transaction'
                 '(id serial PRIMARY KEY,'
                 'date DATE NOT NULL,'
                 'country VARCHAR(5) NOT NULL,'
                 'symbol VARCHAR(15) NOT NULL,'
                 'type VARCHAR(5) NOT NULL,'
                 'quantity REAL NOT NULL,'
                 'price REAL NOT NULL,'
                 'crypto BOOLEAN NOT NULL,'
                 'total_amount REAL NOT NULL);')
        self.run_query(query)

    def copy_from_csv(self, table: str, filename: str) -> None:
        path = f'./{filename}'
        abs_path = os.path.abspath(path)
        query = (f"COPY {table} "
                 f"FROM '{abs_path}' "
                  "DELIMITER ',' "
                  "CSV HEADER;")
        self.run_query(query)

    def get_column_name(self, table: str) -> list:
        try:
            query = f'SELECT * FROM {table} LIMIT 0;'
            self.run_query(query)
            col_name = [desc[0] for desc in self.cur.description]
        except Exception as e:
            print(e)
        finally:
            return col_name

    def show_table(self, table: str) -> None:
        try:
            col_name = self.get_column_name(table)
            query = f'SELECT * FROM {table};'
            self.run_query(query)
            result = self.cur.fetchall()
            rows = []
            for item in result:
                rows.append(item)
        except Exception as e:
            print(e)
        finally:
            table = pd.DataFrame(rows, columns=col_name)
            print(table)


    def __del__(self) -> None:
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def __repr__(self) -> str:
        return f"PostgreSQL(database_url='{self.database_url}')"