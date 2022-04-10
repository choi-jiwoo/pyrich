from pyrich.api import set_finnhub


def get_from_us_market(symbol: str):
    # https://finnhub.io/docs/api/quote
    finnhub = set_finnhub()
    price_now = finnhub.quote(symbol)
    return price_now

