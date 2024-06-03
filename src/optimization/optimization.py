# src/backtesting/optimization.py

import vectorbt as vbt
import pandas as pd
from src.strategy.strategy import bollinger_band_strategy

def optimize_strategy(datafile):
    data = pd.read_csv(datafile, index_col='timestamp', parse_dates=True)
    close = data['close']
    volume = data['volume']

    params = {
        'bb_length': range(10, 51),
        'bb_stddev': [i / 10 for i in range(10, 31)],
        'vol_length': range(10, 51),
        'vol_multiplier': [i / 10 for i in range(10, 31)],
        'rsi_length': range(10, 31),
        'rsi_threshold_dev': range(1, 21),
        'atr_length': range(10, 31),
        'atr_multiplier': [i / 10 for i in range(10, 31)],
        'partial_tp_pct': [i / 10 for i in range(1, 10)]
    }

    bbands = vbt.BBANDS.run_combs(close, window=params['bb_length'], std=params['bb_stddev'])
    entries, exits = bollinger_band_strategy(close, volume, None, None, 
                                             bb_length=params['bb_length'], bb_stddev=params['bb_stddev'], 
                                             vol_length=params['vol_length'], vol_multiplier=params['vol_multiplier'], 
                                             rsi_length=params['rsi_length'], rsi_threshold_dev=params['rsi_threshold_dev'], 
                                             atr_length=params['atr_length'], atr_multiplier=params['atr_multiplier'], 
                                             partial_tp_pct=params['partial_tp_pct'])

    pf = vbt.Portfolio.from_signals(close, entries, exits, init_cash=10000)
    stats = pf.total_return()
    best_params = stats.idxmax()

    return best_params

if __name__ == "__main__":
    best_params = optimize_strategy('data/BTCUSDT_5m.csv')
    print(f"Best parameters: {best_params}")
