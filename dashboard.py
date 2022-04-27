import streamlit as st
from streamlit_option_menu import option_menu
from pyrich.portfolio import Portfolio
from pyrich.dividend import Dividend


portfolio = Portfolio('Choi Ji Woo', 'transaction')
st.title(f'Hello {portfolio.name} 👋🏼')

with st.sidebar:
    # https://icons.getbootstrap.com/
    selected = option_menu(
        menu_title='Main Menu',
        options=[
            'Dashboard',
            'Portfolio',
            'My Asset',
            'Transaction History',
            'Dividend History',
            ], 
        icons=['house', 'stack', 'stack', 'stack', 'stack'],
        menu_icon='list',
        default_index=0
    )

if selected == 'Dashboard':
    st.header('Dashboard')
elif selected == 'Portfolio':
    st.header('Portfolio')
elif selected == 'My Asset':
    st.header('My Asset')
elif selected == 'Transaction History':
    st.header('Transaction History')
    transaction_history = portfolio.record
    st.dataframe(transaction_history)
elif selected == 'Dividend History':
    st.header('Dividend History')
    dividend = Dividend('dividend')
    dividend_history = dividend.record
    st.dataframe(dividend_history)