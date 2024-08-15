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
        st.write("Response Snippet:", response.text[:1000])  # Show first 1000 characters of the response
        
        # Check if the response is HTML or JSON
        if 'text/html' in response.headers['Content-Type']:
            # Parse HTML to extract announcements
            soup = BeautifulSoup(response.text, 'html.parser')
            announcements = []
            for item in soup.find_all('div', class_='announcement-item'):
                date = item.find('span', class_='date').text.strip()
                title = item.find('a', class_='announcement-title').text.strip()
                link = item.find('a', class_='announcement-title')['href']
                announcements.append({'Date': date, 'Title': title, 'Link': link})
            return pd.DataFrame(announcements)
        else:
            # Assuming JSON response
            return pd.json_normalize(response.json())
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
        if any("Trading Halt" in title for title in df['Title']):
            st.markdown(f"**Ticker {selected_ticker} has a 'Trading Halt' announcement.**")
        else:
            st.markdown(f"**Ticker {selected_ticker} does not have a 'Trading Halt' announcement.**")
    else:
        st.write("No announcements found or there was an error fetching the data.")
