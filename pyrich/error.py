class EmptySymbolError(Exception):

    def __init__(self, msg: str, *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


class ArrayLengthDoesNotMatchError(Exception):

    def __init__(self, msg: str, *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)