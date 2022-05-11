import pandas as pd
from functools import cached_property
from pyrich.database import PostgreSQL
from pyrich import stock


class Record:

    def __init__(self, table: str) -> None:
        self.table = table
        self.db = PostgreSQL()

    @cached_property
    def record(self) -> pd.DataFrame:
        return self.db.show_table(self.table)

    @property
    def forex_usd_to_won(self) -> float:
        return stock.get_usd_to_krw()

    def __repr__(self) -> str:
        return f"Record(table='{self.table}')"