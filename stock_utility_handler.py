import pandas as pd
import numpy as np

class StockAnalyzer:
    def json_to_dataframe(self, market_data, stock, market):
        df = pd.DataFrame(market_data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        df = df.sort_index()

        # Calculate Moving Averages
        df["7_day_MA"] = df["4. close"].rolling(window=7).mean()
        df["20_day_MA"] = df["4. close"].rolling(window=20).mean()
        df["100_day_MA"] = df["4. close"].rolling(window=100).mean()
        df["200_day_MA"] = df["4. close"].rolling(window=200).mean()

        # Fibonacci Retracement Levels (using last 100 days)
        df_recent = df.tail(100)
        max_price = df_recent["4. close"].max()
        min_price = df_recent["4. close"].min()
        
        df["fib_0"] = min_price
        df["fib_23.6"] = min_price + (max_price - min_price) * 0.236
        df["fib_38.2"] = min_price + (max_price - min_price) * 0.382
        df["fib_50"] = min_price + (max_price - min_price) * 0.5
        df["fib_61.8"] = min_price + (max_price - min_price) * 0.618
        df["fib_100"] = max_price

        return df
