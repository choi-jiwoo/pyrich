import pandas as pd
import numpy as np
from pyrich.record import Record


class Portfolio(Record):

    def __init__(self, name: str, table: str) -> None:
        super().__init__(table)
        self.name = name

    def _get_pivot_table(self, column: str, remove_na: bool=False) -> pd.DataFrame:
        record_pivot_table = pd.pivot_table(
            self.record,
            values=column,
            index='symbol',
            columns='type',
            aggfunc=np.sum
        )
        if remove_na:
            record_pivot_table.fillna(0, inplace=True)
        return record_pivot_table

    def _get_current_stock(self) -> pd.DataFrame:
        stock = self._get_pivot_table('quantity', remove_na=True)
        stock['amount'] = stock['buy'] - stock['sell']
        return stock

    def _get_earnings(self) -> pd.DataFrame:
        earnings = self._get_pivot_table('total_amount')
        earnings['amount'] = earnings['sell'] - earnings['buy']
        return earnings
    
    def summary(self) -> pd.DataFrame:
        quantity = self._get_current_stock()
        quantity = quantity[quantity['amount'] > 0]
        quantity = quantity['amount']

        earnings = self._get_earnings()
        earnings = earnings[earnings['amount'].isna()]
        total_amount = earnings['buy']

        data = {'quantity': quantity, 'total_amount': total_amount}
        summary = pd.DataFrame(data)
        return summary

    def __repr__(self) -> str:
        return f"Portfolio(name='{self.name}', table='{self.table}')"