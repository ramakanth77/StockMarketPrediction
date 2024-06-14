# stocks/views.py
import requests
from django.shortcuts import render
from .forms import StockForm
import matplotlib.pyplot as plt
import io
import base64

def fetch_stock_data(ticker):
    response = requests.post('http://127.0.0.1:5000/get_stock_data', json={'ticker': ticker})
    return response.json()

def plot_stock_data(data):
    dates = [item['Date'] for item in data]
    close_prices = [item['Close'] for item in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, close_prices, label='Close Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Stock Prices Over Time')
    plt.legend()

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
            data = fetch_stock_data(ticker)
            if 'error' not in data:
                graph = plot_stock_data(data)
    else:
        form = StockForm()

    return render(request, 'stocks/stock.html', {'form': form, 'graph': graph,'name':name})
