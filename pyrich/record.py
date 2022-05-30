from datetime import datetime
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

    def record_current_asset(self, current_asset: float) -> None:
        today = datetime.today()
        timestamp = today.strftime('%Y-%m-%d')
        record = {
            'date': timestamp,
            'amount': current_asset,
        }
        self.db.insert('current_asset', record, msg=False)

    def __repr__(self) -> str:
        return f"Record(table='{self.table}')"
