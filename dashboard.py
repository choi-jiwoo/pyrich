import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from pyrich.portfolio import Portfolio
from pyrich.dividend import Dividend
from pyrich.cash import Cash


pd.set_option('styler.format.precision', 2)
pd.set_option('styler.format.thousands', ',')

# Loading main page
portfolio = Portfolio('Choi Ji Woo', 'transaction')
st.title(f'Hello {portfolio.name} 👋🏼')

# Loding portfolio data
portfolio_table = portfolio.current_portfolio()
portfolio_value = portfolio.get_current_portfolio_value(portfolio_table)

# Sidebar component
with st.sidebar:
    # https://icons.getbootstrap.com/
    selected = option_menu(
        menu_title='Main Menu',
        options=[
            'Dashboard',
            'Portfolio',
            'My Asset',
            'Dividends',
            'Transaction History',
            ], 
        icons=['house', 'stack', 'stack', 'stack', 'stack'],
        menu_icon='list',
        default_index=0
    )

if selected == 'Dashboard':
    st.header('Dashboard')
elif selected == 'Portfolio':
    st.header('Portfolio')
    st.subheader('Portfolio Value')

    current_yield = portfolio_value['portfolio_gain'] / portfolio_value['invested_amount']
    color = '#fff'
    if current_yield < 0:
        color = '#a50e0e' # red
    elif current_yield > 0:
        color = '#137333' # green

    current_value_text = ("<span style='font-weight: bold; font-size: 42px;'>"
                          f"{portfolio_value['current_value']:,.2f}원"
                          "</span>"
                          f"<span style='color: {color};'>"
                          f"&nbsp;{portfolio_value['portfolio_gain']:,.2f}원"
                          f"&nbsp;({current_yield:,.2%})"
                          "</span>")
    st.markdown(current_value_text, unsafe_allow_html=True)

    st.subheader('Current portfolio')
    value_subset = ['day_change(%)', 'pct_gain(%)', 'total_gain']
    styled_portfolio_table = portfolio_table.style.applymap(Portfolio.style_change, subset=value_subset)
    st.table(styled_portfolio_table)
elif selected == 'My Asset':
    st.header('My Asset')

    # cash
    cash = Cash('cash')
    cash_table = cash.record
    total_cash = cash.get_total_cash_in_krw()

    # stock
    investment_by_country = portfolio.get_investment_by_country(portfolio_table)
    total_stock_value = pd.Series(portfolio_value['current_value'], index=['total_stock_value'], dtype=float)

    # total asset
    asset_table = pd.concat([total_cash, total_stock_value])
    total_asset = asset_table.agg({'total_asset': np.sum})
    total_asset_table = pd.concat([asset_table, total_asset]).to_frame(name='Values in KRW')
    st.table(total_asset_table)

    st.header('Asset Details')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Cash')
        cash_table.drop(columns='id', inplace=True)
        st.table(cash_table)
    with col2:
        st.subheader('Investment')
        styled_investment_by_country = investment_by_country.style.applymap(Portfolio.style_change, subset='total_gain')
        st.table(styled_investment_by_country)
elif selected == 'Transaction History':
    st.header('Transaction History')
    transaction_history = portfolio.record
    transaction_history.drop('id', axis=1, inplace=True)
    export_to_csv = transaction_history.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        'export to csv',
        export_to_csv,
        'transaction_history.csv',
        'text/csv',
    )
    st.dataframe(transaction_history)
elif selected == 'Dividends':
    st.header('Dividends')
    dividend = Dividend('dividend')
    dividend_history = dividend.record
    dividend_history.drop('id', axis=1, inplace=True)

    st.subheader('Total Dividends Received')
    total_dividends = dividend.get_total_dividends()
    total_dividends = {'Value in KRW': [total_dividends]}
    total_dividends_table = pd.DataFrame(total_dividends, index=['total_dividends'])
    st.table(total_dividends_table)

    st.subheader('Total Dividends Received by Stock')
    dividends_by_stock = dividend.get_dividends_received_by_stock()
    st.table(dividends_by_stock)

    st.subheader('Dividends History')
    export_to_csv = dividend_history.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        'export to csv',
        export_to_csv,
        'dividend_history.csv',
        'text/csv',
    )
    st.dataframe(dividend_history)