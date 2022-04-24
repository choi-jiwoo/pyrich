from pyrich.error import EmptySymbolError


class Transaction:

    def __init__(self, record: dict) -> None:
        self.record = record

    @property
    def record(self) -> dict:
        return self._record

    @record.setter
    def record(self, record: dict) -> None:
        try:
            record['symbol'] = record['symbol'].upper()
            record['country'] = record['country'].upper()
        except (AttributeError, TypeError):
            raise EmptySymbolError('Symbol is not provided.')
        else:
            self._record = record

    def record_dividends(self, column: list) -> dict:
        dividend_record = dict.fromkeys(column)
        items = self.record.items()
        for item in items:
            if item[0] in dividend_record:
                dividend_record[item[0]] = item[1]
        dividend_record['dividend'] = dividend_record.pop('price')
        return dividend_record

