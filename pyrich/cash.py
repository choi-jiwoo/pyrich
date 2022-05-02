import pandas as pd
from pyrich.record import Record


class Cash(Record):

    def __init__(self, table: str) -> None:
        super().__init__(table)

    def __repr__(self) -> str:
        return f"Cash(table='{self.table}')"
