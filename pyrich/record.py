import pandas as pd
from pyrich.database import PostgreSQL


class Record:

    def __init__(self, table: str) -> None:
        self.table = table
        self.db = PostgreSQL()

    @property
    def record(self) -> pd.DataFrame:
        return self.db.show_table(self.table)

    def __repr__(self) -> str:
        return f"Record(table='{self.table}')"