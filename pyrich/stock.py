from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from pyrich.api import set_finnhub
from pyrich.error import SearchError

HEADERS = {
    'User-Agent': 'Mozilla',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded'
}

def get_current_price(stock: dict) -> float:
    if stock['country'] == 'USA':
        price_now = get_from_us_market(stock['symbol'])
    elif stock['country'] == 'KOR':
        price_now = get_from_kor_market(stock['symbol'])
    elif stock['country'] == 'CRYPTO':
        crypto_symbol = f"BINANCE:{stock['symbol']}USDT"
        price_now = get_from_us_market(crypto_symbol)
    else:
        raise SearchError('Company name not found.')
    return price_now

def get_from_us_market(symbol: str):
    # https://finnhub.io/docs/api/quote
    finnhub = set_finnhub()
    quote = finnhub.quote(symbol)
    current_price = quote['c']
    return current_price

def search_kor_company_symbol(company_name: str) -> tuple:
    url = 'https://kind.krx.co.kr/common/searchcorpname.do'
    data = {
        'method': 'searchCorpNameJson',
        'searchCodeType': 'char',
        'searchCorpName': company_name,
    }
    res = requests.post(url, headers=HEADERS, data=data)
    try:
        res_data = res.json()
        first_search_res = res_data[0]
        official_comp_name = first_search_res['repisusrtkornm']
        comp_symbol = first_search_res['repisusrtcd2']
        return official_comp_name, comp_symbol
    except Exception:
        res.raise_for_status()

def search_us_company_symbol(company_name: str) -> tuple:
    url = 'https://efts.sec.gov/LATEST/search-index'
    form_data = f'{{"keysTyped": "{company_name}","narrow": true}}'
    res = requests.post(url, data=form_data)
    try:
        res_data = res.json()
        search_result = res_data['hits']['hits']
        top_result = search_result[0]
        stock_info = top_result['_source']
        official_company_name = stock_info['entity']
        official_company_name = re.sub(
            r'\s\(\w*\)',
            '',
            official_company_name,
            flags=re.IGNORECASE
        )
        comp_symbol = stock_info['tickers']
        return official_company_name, comp_symbol
    except Exception:
        res.raise_for_status()

def get_symbol(company_name: str, country: str='USA') -> tuple:
    if country == 'USA':
        comp = search_us_company_symbol(company_name)
    elif country == 'KOR':
        comp = search_kor_company_symbol(company_name)
    else:
        raise SearchError('Company name not found.')
    return comp

def scrape_from_naver_finance(symbol: str):
    url = f'https://finance.naver.com/item/main.nhn?code={symbol}'
    res = requests.get(url)
    res.raise_for_status()
    html = res.text
    soup = bs(html, 'html.parser')
    today = soup.select_one('#chart_area > div.rate_info > div')
    tags = today.find_all('span', class_='blind')
    return tags

def get_from_kor_market(symbol: str):
    info = scrape_from_naver_finance(symbol)
    data = []
    for tag in info:
        item = tag.get_text()
        item = item.replace(',', '')
        data.append(float(item))
    current_price_and_pct_change = ['c', 'dp']  # c: current price, dp: percent change
    price_data = {k: v for k, v in zip(label, data)}
    return price_data

def get_usd_to_krw():
    url = 'https://finance.naver.com/marketindex/exchangeDetail.naver?marketindexCd=FX_USDKRW'
    naver_finance_currency_data = pd.read_html(url)
    currency_table = naver_finance_currency_data[0]
    current_usd_to_krw = currency_table.iloc[0, 0]
    return current_usd_to_krw
