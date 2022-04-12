from bs4 import BeautifulSoup as bs
import requests
from pyrich.api import set_finnhub


def get_current_price(stock: dict) -> float:
    if stock['country'] == 'USA':
        price_now = get_from_us_market(stock['symbol'])
    elif stock['country'] == 'KOR':
        price_now = get_from_kor_market(stock['symbol'])
    return price_now

def get_from_us_market(symbol: str):
    # https://finnhub.io/docs/api/quote
    finnhub = set_finnhub()
    price_now = finnhub.quote(symbol)
    return price_now

def get_from_kor_market(symbol: str):
    info = scrape_from_naver_finance(symbol)
    data = []
    for tag in info:
        item = tag.get_text()
        item = item.replace(',', '')
        data.append(float(item))
    label = ['c', 'd', 'dp']  # c: current price, d: change, dp: percent change
    price_now = {k: v for k, v in zip(label, data)}
    return price_now

def scrape_from_naver_finance(symbol: str):
    url = f'https://finance.naver.com/item/main.nhn?code={symbol}'
    res = requests.get(url)
    res.raise_for_status()
    html = res.text
    soup = bs(html, 'html.parser')
    today = soup.select_one('#chart_area > div.rate_info > div')
    tags = today.find_all('span', class_='blind')
    return tags
