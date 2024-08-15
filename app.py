# app.py

# Imports
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Function to fetch announcements using Selenium
def fetch_announcements(ticker):
    url = f'https://www.asx.com.au/asx/1/company/{ticker}/announcements?count=20&market_sensitive=false'
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    
    # Parse announcements
    announcements = []
    try:
        items = driver.find_elements(By.CLASS_NAME, 'announcement-item')
        for item in items:
            date = item.find_element(By.CLASS_NAME, 'date').text.strip()
            title = item.find_element(By.CLASS_NAME, 'announcement-title').text.strip()
            link = item.find_element(By.CLASS_NAME, 'announcement-title').get_attribute('href')
            announcements.append({'Date': date, 'Title': title, 'Link': link})
    except Exception as e:
        st.error(f"Error fetching announcements: {e}")
    
    driver.quit()
    return pd.DataFrame(announcements)

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
