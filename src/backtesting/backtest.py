# src/backtesting/backtest.py

import vectorbt as vbt
import pandas as pd
from src.strategy.strategy import bollinger_band_strategy, apply_stop_loss_take_profit

def run_backtest(datafile, bb_length, bb_stddev, vol_length, vol_multiplier, 
                 rsi_length, rsi_threshold_dev, atr_length, atr_multiplier, partial_tp_pct):
    data = pd.read_csv(datafile, index_col='timestamp', parse_dates=True)
    close = data['close']
    volume = data['volume']
    
    long_entries, long_exits, short_entries, short_exits, atr_upper_bound, atr_lower_bound, partial_tp_pct = \
        bollinger_band_strategy(close, volume, None, None, 
                                bb_length, bb_stddev, 
                                vol_length, vol_multiplier, 
                                rsi_length, rsi_threshold_dev, 
                                atr_length, atr_multiplier, partial_tp_pct)

    pf = vbt.Portfolio.from_signals(close, long_entries, long_exits, short_entries, short_exits, 
                                    init_cash=10000)
    pf = apply_stop_loss_take_profit(pf, atr_upper_bound, atr_lower_bound, partial_tp_pct)
    
    print(pf.stats())
    pf.plot().show()

if __name__ == "__main__":
    datafile = 'data/BTCUSDT_5m.csv'
    run_backtest(datafile, bb_length=20, bb_stddev=2, vol_length=20, vol_multiplier=1.5, 
                 rsi_length=14, rsi_threshold_dev=5, atr_length=14, atr_multiplier=1.5, partial_tp_pct=0.5)
