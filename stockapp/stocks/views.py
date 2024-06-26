from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from .models import Stock, Holding, StockHistory
from .forms import StockForm, SignUpForm, LoginForm, HoldingForm
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import requests
import threading
import time

# Use the Agg backend for Matplotlib
#matplotlib.use('Agg')

IST = timezone.get_default_timezone()


def predict_stock(request, ticker):
    if not request.user.is_authenticated:
        return redirect('login')

    response = requests.post('http://127.0.0.1:5000/predict', json={'ticker': ticker})
    prediction = response.json()

    if 'error' in prediction:
        return JsonResponse({'error': prediction['error']})
    else:
        return JsonResponse({'prediction': prediction['prediction']})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')




def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.history(period="1d")
    return info.reset_index().to_dict(orient='records')

def holdings(request):
    if request.method == 'POST':
        form = HoldingForm(request.POST)
        if form.is_valid():
            stock = form.cleaned_data.get('stock')
            quantity = form.cleaned_data.get('quantity')

            # Fetch the current price
            current_price_list = get_stock_data(stock.ticker)
            current_price = 0
            if len(current_price_list) > 0:
                full_details_dict = current_price_list[0]
                current_price = full_details_dict['Close']

            # Check for existing holdings
            existing_holdings = Holding.objects.filter(user=request.user, stock=stock)
            if existing_holdings.exists():
                holding = existing_holdings.first()
                if quantity == 0:
                    holding.delete()
                else:
                    total_quantity = holding.quantity + quantity
                    holding.purchase_price = (holding.purchase_price * holding.quantity + current_price * quantity) / total_quantity
                    holding.quantity = total_quantity
                    holding.stock.current_price_inr = float(current_price)
                    holding.save()
            else:
                # If no existing holding, create a new one
                holding = form.save(commit=False)
                holding.user = request.user
                holding.purchase_price = float(current_price)
                holding.stock.current_price_inr = float(current_price)
                holding.save()

            return redirect('holdings')
    else:
        form = HoldingForm()

    user_holdings = Holding.objects.filter(user=request.user)
    total_value = 0.0
    total_invested = 0.0

    for holding in user_holdings:
        current_price_list = get_stock_data(holding.stock.ticker)
        current_price = 0
        if len(current_price_list) > 0:
            full_details_dict = current_price_list[0]
            current_price = full_details_dict['Close']
        holding.stock.current_price_inr = float(current_price)
        holding.total_value = float(holding.quantity) * float(current_price)
        holding.save()
        total_value += holding.total_value
        total_invested += holding.quantity * holding.purchase_price

    total_gain_loss = total_value - total_invested

    return render(request, 'holdings.html', {
        'form': form,
        'holdings': user_holdings,
        'total_value': round(total_value, 2),
        'total_invested': round(total_invested, 2),
        'total_gain_loss': round(total_gain_loss, 2)
    })

def update_prices(request):
    user_holdings = Holding.objects.filter(user=request.user)
    for holding in user_holdings:
        current_price_list = get_stock_data(holding.stock.ticker)
        current_price = 0
        if len(current_price_list) > 0:
            full_details_dict = current_price_list[0]
            current_price = full_details_dict['Close']
        holding.stock.current_price_inr = float(current_price)
        holding.total_value = float(holding.quantity) * float(current_price)
        holding.stock.save()
        holding.save()
    return JsonResponse({'status': 'updated'})

def get_stock_data(ticker, period='1d', interval='1h'):
    response = requests.post('http://127.0.0.1:5000/get_stock_data',
                             json={'ticker': ticker, 'period': period, 'interval': interval})
    data = response.json()
    if 'error' not in data:
        for entry in data:
            entry['Date'] = pd.to_datetime(entry['Date']).tz_localize('UTC').tz_convert(IST)
        return data
    else:
        return []


def fetch_stock_info(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        'prev_close': info.get('previousClose'),
        'open': info.get('open'),
        'volume': info.get('volume'),
        'avg_vol_3m': info.get('averageVolume'),
        'pe_ratio': info.get('trailingPE'),
        'market_cap': info.get('marketCap'),
        'beta': info.get('beta')
    }


def fetch_and_update_stock(stock):
    hist_data = get_stock_data(stock.ticker)
    if hist_data:
        hist_df = pd.DataFrame(hist_data)
        hist_df['Close_INR'] = hist_df['Close'].apply(lambda x: round(x, 2))

        current_price_inr = hist_df.iloc[-1]['Close_INR']
        if stock.current_price_inr:
            percent_change = ((current_price_inr - stock.current_price_inr) / stock.current_price_inr) * 100
        else:
            percent_change = 0

        stock.current_price_inr = round(current_price_inr, 2)
        stock.percent_change = round(percent_change, 2)
        stock.save()

        for _, row in hist_df.iterrows():
            naive_time = row['Date'].replace(tzinfo=None)
            StockHistory.objects.create(stock=stock, time=timezone.make_aware(naive_time), price=row['Close_INR'])


def update_stocks_periodically():
    while True:
        for stock in Stock.objects.all():
            fetch_and_update_stock(stock)
        time.sleep(300)


def plot_stock_graph(history, small_graph=False):
    dates = [entry['Date'] for entry in history]
    close_prices = [entry['Close'] for entry in history]

    plt.ioff()
    if small_graph:
        plt.figure(figsize=(3, 1))
        plt.plot(dates, close_prices, linewidth=1)
        plt.axis('off')
    else:
        plt.figure(figsize=(10, 5))
        plt.plot(dates, close_prices, label='Close Price')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.title('Stock Prices Over Time')
        plt.legend()
        plt.gcf().autofmt_xdate()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graph = base64.b64encode(image_png).decode('utf-8')
    return graph


def index(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = StockForm()

    if request.method == 'GET' and 'delete' in request.GET:
        stock_id = request.GET.get('delete')
        Stock.objects.filter(id=stock_id).delete()
        return redirect('index')

    stocks = Stock.objects.all()

    return render(request, 'index.html', {'form': form, 'stocks': stocks})


def stock_detail(request, stock_id, period='1d'):
    stock = get_object_or_404(Stock, id=stock_id)
    interval = '1h' if period in ['1d', '5d'] else '1d'
    hist_data = get_stock_data(stock.ticker, period=period, interval=interval)

    hist_df = pd.DataFrame(hist_data)
    if 'Date' in hist_df.columns:
        hist_df.set_index('Date', inplace=True)
    hist_df['Close'] = hist_df['Close'].apply(lambda x: round(x, 2))

    history = hist_df.reset_index()[['Date', 'Close']].to_dict(orient='records')
    graph = plot_stock_graph(history, small_graph=False)

    stock_info = fetch_stock_info(stock.ticker)

    return render(request, 'stock_detail.html', {
        'stock': stock,
        'history': history,
        'period': period,
        'graph': graph,
        'stock_info': stock_info
    })


threading.Thread(target=update_stocks_periodically, daemon=True).start()
