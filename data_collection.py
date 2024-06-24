import yfinance as yf

def fetch_stock_data(ticker, period='1y', interval='1d'):
    data = yf.download(ticker, period=period, interval=interval)
    if data.empty:
        raise ValueError("No data found for the given ticker and period.")
    return data
