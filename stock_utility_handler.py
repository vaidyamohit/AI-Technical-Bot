import pandas as pd
import json
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.widgets as widgets
import requests

class StockAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_stock_info(self, stock, market):
        if market == 'NASDAQ':
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&outputsize=compact&apikey={self.api_key}'
        else:
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}.{market}&outputsize=compact&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        return data

class StockAnalyzer:
    def __init__(self):
        pass

    def json_to_dataframe(self, json_data, stock_symbol, market):
        print(json_data)
        time_series_data = json_data['Time Series (Daily)']
        df_data = []

        for date_str, values in time_series_data.items():
            data_row = {'date': date_str}
            for key, value in values.items():
                new_key = key.split('. ')[1]
                data_row[new_key] = float(value)
            df_data.append(data_row)

        df = pd.DataFrame(df_data)
        df['date'] = pd.to_datetime(df['date'])

        eastern = pytz.timezone('US/Eastern')
        ist = pytz.timezone('Asia/Kolkata')

        df['date'] = df['date'].dt.tz_localize(eastern).dt.tz_convert(ist)
        df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['stock'] = stock_symbol
        df['market'] = market

        df = df.set_index('date')
        
        df['MA_7'] = df['close'].rolling(window=7).mean()
        df['MA_20'] = df['close'].rolling(window=20).mean()
        df['MA_100'] = df['close'].rolling(window=100).mean()
        df['MA_200'] = df['close'].rolling(window=200).mean()
        
        return df

    def calculate_fibonacci_levels(self, df):
        max_price = df['close'].max()
        min_price = df['close'].min()
        diff = max_price - min_price

        levels = {
            '0.0%': max_price,
            '23.6%': max_price - (0.236 * diff),
            '38.2%': max_price - (0.382 * diff),
            '50.0%': max_price - (0.5 * diff),
            '61.8%': max_price - (0.618 * diff),
            '78.6%': max_price - (0.786 * diff),
            '100.0%': min_price
        }
        return levels

    def generate_trade_signal(self, df, fib_levels):
        latest_close = df['close'].iloc[-1]
        ma_100 = df['MA_100'].iloc[-1]
        ma_200 = df['MA_200'].iloc[-1]
        
        buy_signal = latest_close > ma_100 and latest_close > ma_200 and latest_close > fib_levels['50.0%']
        sell_signal = latest_close < ma_100 and latest_close < ma_200 and latest_close < fib_levels['50.0%']
        
        if buy_signal:
            return "BUY 📈 - Price above 100/200 DMA and key Fibonacci level"
        elif sell_signal:
            return "SELL 📉 - Price below 100/200 DMA and key Fibonacci level"
        else:
            return "HOLD ⏳ - Price in consolidation phase"

    def plot_stock_data(self, df, stock_symbol, market, image_path, fib_levels):
        plt.figure(figsize=(16, 12))

        plt.subplot(3, 1, 1)
        plt.plot(pd.to_datetime(df.index), df['close'], label=f'{stock_symbol} Closing Price ({market})', color='blue')
        plt.title(f'{stock_symbol} Stock Performance ({market})')
        plt.xlabel('Date (IST)')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        for level, price in fib_levels.items():
            plt.axhline(y=price, linestyle='--', alpha=0.6, label=f'Fib {level}')

        plt.legend()

        plt.subplot(3, 1, 2)
        plt.bar(pd.to_datetime(df.index), df['volume'], label=f'{stock_symbol} Volume ({market})', color='green', width=2)
        plt.xlabel('Date (IST)')
        plt.ylabel('Volume')
        plt.legend()
        plt.grid(True)

        plt.subplot(3, 1, 3)
        plt.plot(pd.to_datetime(df.index), df['close'], label=f'{stock_symbol} Closing Price ({market})', color='blue', alpha=0.7)
        plt.plot(pd.to_datetime(df.index), df['MA_7'], label='7-Day MA', color='orange')
        plt.plot(pd.to_datetime(df.index), df['MA_20'], label='20-Day MA', color='red')
        plt.plot(pd.to_datetime(df.index), df['MA_100'], label='100-Day MA', color='purple', linestyle='dashed')
        plt.plot(pd.to_datetime(df.index), df['MA_200'], label='200-Day MA', color='brown', linestyle='dashed')
        plt.xlabel('Date (IST)')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)

        for ax in plt.gcf().axes:
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=[0]))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.gcf().autofmt_xdate()

        cursor = widgets.Cursor(plt.gca(), color='red', linewidth=1)

        plt.tight_layout()
        plt.savefig(image_path)
        plt.show()
