import streamlit as st
from pyrich.database import PostgreSQL

db = PostgreSQL()
st.title('Streamlit Application')

# Record history
st.header('Transaction History')
transaction_history = db.show_table('transaction')
st.dataframe(transaction_history)

st.header('Dividend History')
dividend_history = db.show_table('dividend')
st.dataframe(dividend_history)