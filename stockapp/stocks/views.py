import requests
from django.shortcuts import render
from .forms import StockForm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64


def fetch_stock_data(ticker, period='1d'):
    response = requests.post('http://127.0.0.1:5000/get_stock_data', json={'ticker': ticker, 'period': period})
    return response.json()


def plot_stock_data(data, period):
    dates = [item['Date'] for item in data]
    close_prices = [item['Close'] for item in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, close_prices, label='Close Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Stock Prices Over Time')
    plt.legend()

    # Adjust date formatting based on period
    if period == '1d' or period == '5d':
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%a'))
    elif period == '1mo':
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    elif period == '3mo' or period == '6mo' or period == '1y':
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    plt.gcf().autofmt_xdate()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    return graph


def stock_view(request):
    graph = None
    name = None
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            name = form.cleaned_data['name']
            period = form.cleaned_data['period']
            data = fetch_stock_data(ticker, period)
            if 'error' not in data:
                graph = plot_stock_data(data, period)
    else:
        form = StockForm()

    return render(request, 'stocks/stock.html', {'form': form, 'graph': graph, 'name': name})
