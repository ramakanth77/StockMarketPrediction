import yfinance as yf

def get_stock_info(ticker):
    # Fetch the stock data for today
    stock = yf.Ticker(ticker)
    todays_data = stock.history(period='1d')

    # Get the current price
    current_price = todays_data['Close'].iloc[-1]

    # Get the previous close price
    previous_close = todays_data['Close'].iloc[0]

    # Calculate the price change
    price_change = current_price - previous_close

    # Calculate the percentage change
    percentage_change = (price_change / previous_close) * 100

    return {
        'ticker': ticker,
        'current_price': current_price,
        'price_change': price_change,
        'percentage_change': percentage_change
    }

# Fetch and display the stock info for JPPOWER.BO
ticker = 'JPPOWER.BO'
stock_info = get_stock_info(ticker)

print(f"Stock Ticker: {stock_info['ticker']}")
print(f"Current Price: {stock_info['current_price']:.2f} INR")
print(f"Price Change: {stock_info['price_change']:.2f} INR")
print(f"Percentage Change: {stock_info['percentage_change']:.2f}%")
