# src/data/collect_data.py

import ccxt
import pandas as pd
from datetime import datetime

def fetch_binance_usdm_symbols():
    binance_usdm = ccxt.binanceusdm()
    markets = binance_usdm.load_markets()
    symbols = [symbol for symbol in markets if markets[symbol]['quote'] == 'USDT']
    return symbols

def fetch_binance_futures_ohlcv(symbol, timeframe, start_date):
    binance_usdm = ccxt.binanceusdm()
    since = binance_usdm.parse8601(f'{start_date}T00:00:00Z')
    now = binance_usdm.milliseconds()

    all_ohlcv = []
    while since < now:
        try:
            ohlcv = binance_usdm.fetch_ohlcv(symbol, timeframe, since)
            if not ohlcv:
                break
            since = ohlcv[-1][0] + binance_usdm.parse_timeframe(timeframe) * 1000
            all_ohlcv += ohlcv
        except Exception as e:
            print(f'Error fetching data for {symbol}: {e}')
            break

    return all_ohlcv

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.to_csv(filename, index=False)

def main():
    symbols = fetch_binance_usdm_symbols()
    symbol = input("Enter the ticker symbol you want to collect data for (e.g., BTC/USDT): ").upper()
    if symbol not in symbols:
        print("Invalid ticker symbol.")
        return
    
    timeframe = input("Enter the timeframe (e.g., 5m, 15m, 1h, 1d): ")
    start_date = input("Enter the start date (YYYY-MM-DD) or type 'earliest' for the earliest possible start date: ")
    
    if start_date.lower() == 'earliest':
        start_date = '2017-08-17'  # Earliest possible start date for Binance Futures USDM
    else:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

    data = fetch_binance_futures_ohlcv(symbol, timeframe, start_date)
    save_to_csv(data, f'data/{symbol.replace("/", "")}_{timeframe}.csv')
    print(f"Data for {symbol} saved to data/{symbol.replace('/', '')}_{timeframe}.csv")

if __name__ == "__main__":
    main()
