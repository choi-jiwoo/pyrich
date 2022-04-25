from collections.abc import Iterable
from dotenv import load_dotenv
import os
import pandas as pd
import psycopg2
from urllib.parse import urlparse


class PostgreSQL:

    load_dotenv()
    DATABASE_URL = os.environ.get('DATABASE_URL')

    def __init__(self) -> None:
        self._parse_database_url()
        self._connect()
        self._create_transaction_table()
        self._create_dividend_table()

    def _parse_database_url(self) -> None:
        connection_info = urlparse(PostgreSQL.DATABASE_URL)
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

    def run_query(self, query: str, values: Iterable=None,
                  msg: bool=False) -> None:
        try:
            self.cur.execute(query, values)
            self.conn.commit()
        except psycopg2.ProgrammingError:
            raise
        finally:
            if msg:
                print('Query ran successfully.')

    def _create_transaction_table(self) -> None:
        query = ('CREATE TABLE IF NOT EXISTS transaction'
                 '(id serial PRIMARY KEY,'
                 'date DATE NOT NULL,'
                 'country VARCHAR(5) NOT NULL,'
                 'symbol VARCHAR(15) NOT NULL,'
                 'crypto BOOLEAN NOT NULL,'
                 'type VARCHAR(5) NOT NULL,'
                 'quantity REAL NOT NULL,'
                 'price REAL NOT NULL,'
                 'total_amount REAL NOT NULL);')
        self.run_query(query)

    def _create_dividend_table(self) -> None:
        query = ('CREATE TABLE IF NOT EXISTS dividend'
                 '(id serial PRIMARY KEY,'
                 'date DATE NOT NULL,'
                 'symbol VARCHAR(15) NOT NULL,'
                 'dividend REAL NOT NULL);')
        self.run_query(query)

    def copy_from_csv(self, table: str) -> None:
        path = f'./{table}.csv'
        abs_path = os.path.abspath(path)
        query = (f"COPY {table} "
                 f"FROM '{abs_path}' "
                  "DELIMITER ',' "
                  "CSV HEADER;")
        self.run_query(query, msg=True)

    def _get_column_name(self, table: str) -> list:
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
            col_name = self._get_column_name(table)
            query = f'SELECT * FROM {table};'
            self.run_query(query, msg=False)
            result = self.cur.fetchall()
            rows = []
            for item in result:
                rows.append(item)
        except Exception as e:
            print(e)
        finally:
            table = pd.DataFrame(rows, columns=col_name)
            return table

    def insert(self, table: str, record: dict) -> None:
        keys = list(record.keys())
        values = list(record.values())
        column = ', '.join(keys)
        value_seq = ['%s' for i in range(len(values))]
        placeholders = ', '.join(value_seq)
        query = (f"INSERT INTO {table} ({column}) "
                 f"VALUES ({placeholders});")
        self.run_query(query, values, msg=True)

    def delete_rows(self, table: str, all_rows: bool=False) -> None:
        if all_rows:
            query = f'DELETE FROM {table};'
            warning_msg = input('Deleting all rows in the table. Continue? (Y/n): ')
        else:
            query = f'DELETE FROM {table} WHERE id=(SELECT MAX(id) FROM {table});'
            warning_msg = input('Deleting the last row. Continue? (Y/n): ')

        if warning_msg.upper() == 'Y':
            self.run_query(query, msg=True)
        else:
            print('Deleting stopped.')
        
    def __del__(self) -> None:
        self.cur.close()
        self.conn.close()

    def __repr__(self) -> str:
        return f"PostgreSQL(database_url='{self.database_url}')"