import requests
import pandas as pd

def get_stock_data(ticker, period='1d', interval='1h'):
    response = requests.post('http://127.0.0.1:5000/get_stock_data', json={'ticker': ticker, 'period': period, 'interval': interval})
    data = response.json()
    if 'error' not in data:
        for entry in data:
            print(entry)  # Print each entry to verify 'Date' column
            entry['Date'] = pd.to_datetime(entry['Date'])
        return data
    else:
        print(data['error'])

# Test the Flask server
ticker = 'AAPL'
period = '1d'
interval = '1h'
hist_data = get_stock_data(ticker, period, interval)

# Print the returned data
print(hist_data)
