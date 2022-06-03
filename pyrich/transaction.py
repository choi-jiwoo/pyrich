# TODO
# should implement user input type validation


class Transaction:

    def __init__(self, record: list, headers: list) -> None:
        self.headers = headers
        self.record = record

    @property
    def record(self) -> dict:
        return self._record

    @record.setter
    def record(self, record: list) -> None:
        mapped_record = zip(self.headers, record)
        mapped_record = {
            header: item
            for header, item in mapped_record
        }
        self._record = self._convert_items(mapped_record)

    def _convert_items(self, record: dict) -> dict:
        uppercase_items = ['country', 'symbol', 'currency']
        float_items = ['quantity', 'price', 'dividend']
        for item in uppercase_items:
            try:
                record[item] = record[item].upper()
            except KeyError:
                continue

        for item in float_items:
            try:
                record[item] = float(record[item])
            except KeyError:
                continue
        return record
