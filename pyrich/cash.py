import pandas as pd
import numpy as np
from pyrich.record import TransactionRecord


class Cash(TransactionRecord):

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

    def get_total_cash_in_krw(self) -> pd.Series:
        cash_table = self.record.drop(columns='id')
        current_cash = cash_table.set_index('currency')
        current_cash.loc['USD'] *= self.forex_usd_to_won
        current_cash.rename(columns={'amount': 'total_cash'}, inplace=True)
        total_cash_in_krw = np.sum(current_cash)
        return total_cash_in_krw

    def __repr__(self) -> str:
        return f"Cash(table='{self.table}')"
