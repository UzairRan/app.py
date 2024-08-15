# app.py

# Imports
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to fetch announcements
def fetch_announcements(ticker):
    url = f'https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP request errors
        
        # Display response headers and a snippet of the response text for debugging
        st.write("Response Headers:", response.headers)
        st.write("Response Snippet:", response.text[:2000])  # Show first 2000 characters of the response
        
        # Check if the response is HTML
        if 'text/html' in response.headers['Content-Type']:
            # Parse HTML to extract announcements
            soup = BeautifulSoup(response.text, 'html.parser')
            announcements = []
            # Ensure we have the right selectors
            items = soup.find_all('div', class_='announcement-item')
            if not items:
                st.write("No announcements found. Please check the URL or class names.")
            for item in items:
                date = item.find('span', class_='date').text.strip() if item.find('span', class_='date') else 'No Date'
                title = item.find('a', class_='announcement-title').text.strip() if item.find('a', class_='announcement-title') else 'No Title'
                link = item.find('a', class_='announcement-title')['href'] if item.find('a', class_='announcement-title') else 'No Link'
                announcements.append({'Date': date, 'Title': title, 'Link': link})
            return pd.DataFrame(announcements)
        else:
            st.write("Unexpected response format. Expected HTML but received something else.")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return pd.DataFrame()

# List of ticker symbols
tickers = ['AEE', 'REZ', '1AE', '1MC', 'NRZ']

# Streamlit app
st.title('ASX Announcements Viewer')

# Select ticker symbol
selected_ticker = st.selectbox('Select Ticker Symbol', tickers)

# Fetch and display announcements
if st.button('Fetch Announcements'):
    df = fetch_announcements(selected_ticker)
    
    if not df.empty:
        st.write(f"Recent Announcements for {selected_ticker}:")
        st.dataframe(df)
        
        # Identify "Trading Halt" announcements
        if 'Title' in df.columns and any("Trading Halt" in title for title in df['Title']):
            st.markdown(f"**Ticker {selected_ticker} has a 'Trading Halt' announcement.**")
        else:
            st.markdown(f"**Ticker {selected_ticker} does not have a 'Trading Halt' announcement.**")
    else:
        st.write("No announcements found or there was an error fetching the data.")
