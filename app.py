# app.py

import streamlit as st
import requests

# List of ticker symbols
tickers = ['AEE', 'REZ', '1AE', '1MC', 'NRZ']

# Function to retrieve announcements for a ticker
# Function to retrieve announcements for a ticker
def get_announcements(ticker):
    url = f"https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.json().get('announcements', [])
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
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
    if any("Trading Halt" in announcement.get('header', '') for announcement in announcements):
        trading_halt_tickers.append(ticker)

if trading_halt_tickers:
    st.write("**Tickers with 'Trading Halt' announcements:**")
    st.write(", ".join(trading_halt_tickers))
else:
    st.write("No tickers with 'Trading Halt' announcements.")
