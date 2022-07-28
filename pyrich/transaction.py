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
        items = {
            'uppercase': ['country', 'symbol', 'currency'],
            'float': ['quantity', 'price', 'dividend'],
        }
        for key in items:
            for item in items[key]:
                try:
                    if key == 'uppercase':
                        record[item] = record[item].upper()
                    else:
                        record[item] = float(record[item])
                except KeyError:
                    continue
        return record
