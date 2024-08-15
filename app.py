# app.py

# Imports Necessary libraries
import streamlit as st
import requests

# List of ticker symbols
tickers = ['AEE', 'REZ', '1AE', '1MC', 'NRZ']

# Function to retrieve announcements for a ticker
def get_announcements(ticker):
    url = f"https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        
        # Debugging: Print raw response text
        st.write("Raw response:", response.text[:2000])  # Print the first 2000 characters for brevity

        # Attempt to parse JSON response
        try:
            data = response.json()
            if 'announcements' in data:
                return data['announcements']
            else:
                st.error(f"No 'announcements' key in the response. Response data: {data}")
                return []
        except ValueError:
            st.error("Error: The response is not in JSON format.")
            return []

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
        st.write(f"**Date:** {announcement.get('date', 'N/A')}")
        st.write(f"**Title:** {announcement.get('header', 'N/A')}")
        st.write(f"**Link:** [View Announcement](https://www.asx.com.au/asxpdf/{announcement.get('id', 'N/A')}.pdf)")
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

