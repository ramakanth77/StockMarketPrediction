import yfinance as yf
import pandas as pd
import os

def download_data(ticker, start_date, end_date):
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            raise ValueError("No data found, check the ticker symbol and date range.")
        return data
    except Exception as e:
        print(f"Error downloading data: {e}")
        return None

def save_data(data, filename):
    try:
        data.to_csv(filename)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data: {e}")

if __name__ == "__main__":
    ticker = 'AAPL'
    start_date = '2010-01-01'
    end_date = '2023-01-01'
    filename = 'AAPL_stock_data.csv'

    data = download_data(ticker, start_date, end_date)
    if data is not None:
        save_data(data, filename)
