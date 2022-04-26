import pandas as pd
from pyrich.database import PostgreSQL


class Portfolio:

    def __init__(self, name: str) -> None:
        self.name = name
        self.db = PostgreSQL()

    def transaction_history(self, table_name: str) -> pd.DataFrame:
        record = self.db.show_table(table_name)
        return record

    def __repr__(self) -> str:
        return f"Portfolio(name='{self.name}')"