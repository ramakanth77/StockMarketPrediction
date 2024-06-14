import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller

def load_data(filename):
    try:
        data = pd.read_csv(filename, index_col='Date', parse_dates=True)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def visualize_data(data):
    try:
        plt.figure(figsize=(14, 7))
        plt.plot(data['Close'], label='Close Price')
        plt.title('Historical Stock Prices')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        plt.show()
    except Exception as e:
        print(f"Error visualizing data: {e}")

def correlation_analysis(data):
    try:
        plt.figure(figsize=(10, 6))
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()
    except Exception as e:
        print(f"Error in correlation analysis: {e}")

def stationarity_check(data, column='Close'):
    try:
        result = adfuller(data[column].dropna())
        print('ADF Statistic:', result[0])
        print('p-value:', result[1])
        for key, value in result[4].items():
            print('Critial Values:')
            print(f'   {key}, {value}')
        if result[1] > 0.05:
            print("The series is non-stationary.")
        else:
            print("The series is stationary.")
    except Exception as e:
        print(f"Error in stationarity check: {e}")

if __name__ == "__main__":
    filename = 'AAPL_stock_data_processed.csv'

    data = load_data(filename)
    if data is not None:
        visualize_data(data)
        correlation_analysis(data)
        stationarity_check(data)
