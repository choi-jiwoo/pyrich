import pandas as pd
from pyrich.record import Record


class Portfolio(Record):

    def __init__(self, name: str, table: str) -> None:
        super().__init__(table)
        self.name = name

    def __repr__(self) -> str:
        return f"Portfolio(name='{self.name}', table='{self.table}')"