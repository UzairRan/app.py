# app.py

import streamlit as st
import requests

# List of ticker symbols
tickers = ['AEE', 'REZ', '1AE', '1MC', 'NRZ']

# Function to retrieve announcements for a ticker
def get_announcements(ticker):
    url = f"https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('announcements', [])
    else:
        return []

# Streamlit app
st.title("ASX Announcements Viewer")

# Select a ticker symbol
selected_ticker = st.selectbox("Select a Ticker", tickers)

# Retrieve announcements for the selected ticker
announcements = get_announcements(selected_ticker)

if announcements:
    st.write(f"**Recent Announcements for {selected_ticker}:**")
    for announcement in announcements:
        st.write(f"**Date:** {announcement['date']}")
        st.write(f"**Title:** {announcement['header']}")
        st.write(f"**Link:** [View Announcement](https://www.asx.com.au/asxpdf/{announcement['id']}.pdf)")
        st.write("---")
else:
    st.write("No announcements found.")

# Identify tickers with 'Trading Halt' announcements
trading_halt_tickers = []
for ticker in tickers:
    announcements = get_announcements(ticker)
    if any("Trading Halt" in announcement['header'] for announcement in announcements):
        trading_halt_tickers.append(ticker)

if trading_halt_tickers:
    st.write("**Tickers with 'Trading Halt' announcements:**")
    st.write(", ".join(trading_halt_tickers))
else:
    st.write("No tickers with 'Trading Halt' announcements.")
