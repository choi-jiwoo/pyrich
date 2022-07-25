from datetime import date
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
    def map_currency(currency_indicator: pd.Series, display_krw: bool = False) -> list:
        currency_mapping = {
            'CRYPTO': 'KRW',
            'KOR': 'KRW',
            'USA': 'USD',
        }
        if display_krw:
            currency_mapping['USA'] = 'KRW'

        currency_map = [
            currency_mapping[country]
            for country
            in currency_indicator
        ]
        return currency_map

    def __repr__(self) -> str:
        return f"Record(table='{self.table}')"
