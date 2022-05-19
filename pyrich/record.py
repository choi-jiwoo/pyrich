import pandas as pd
from functools import cached_property
from pyrich.database import PostgreSQL
from pyrich import forex


class Record:

    def __init__(self, table: str) -> None:
        self.table = table
        self.db = PostgreSQL()

    @cached_property
    def record(self) -> pd.DataFrame:
        return self.db.show_table(self.table)

    @property
    def forex_usd_to_won(self) -> float:
        return forex.get_usd_to_krw()

    @staticmethod
    def style_change(value: float) -> str:
        color = {
            'neg': '#a50e0e',
            'pos': '#137333',
        }
        style = None
        if value > 0:
            style = f"color:{color['pos']};"
        elif value < 0:
            style = f"color:{color['neg']};"
        return style

    def __repr__(self) -> str:
        return f"Record(table='{self.table}')"
