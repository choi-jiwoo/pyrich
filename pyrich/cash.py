import pandas as pd
from pyrich.record import Record


class Cash(Record):

    def __init__(self, table: str) -> None:
        super().__init__(table)

    def update_current_cash(self, column: str, value: str, currency: str) -> None:
        try:
            value = float(value)
        except ValueError:
            value = 0
        finally:
            currency_id = {
                'KRW': 1,
                'USD': 2,
            }
            _id = currency_id[currency]
            self.db.update('cash', [column], [value], _id, msg=False)

    def __repr__(self) -> str:
        return f"Cash(table='{self.table}')"
