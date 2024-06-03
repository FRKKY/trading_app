# src/strategy/strategy.py

import vectorbt as vbt
import numpy as np

def bollinger_band_strategy(close, volume, rsi, atr, 
                            bb_length, bb_stddev, 
                            vol_length, vol_multiplier, 
                            rsi_length, rsi_threshold_dev, 
                            atr_length, atr_multiplier,
                            partial_tp_pct):
    # Bollinger Bands
    bb = vbt.BBANDS.run(close, window=bb_length, std=bb_stddev)

    # Volume Threshold
    vol_sma = vbt.MA.run(volume, window=vol_length).ma
    vol_threshold = vol_sma * vol_multiplier

    # RSI
    rsi = vbt.RSI.run(close, window=rsi_length).rsi
    rsi_upper = 70 + rsi_threshold_dev
    rsi_lower = 30 - rsi_threshold_dev

    # ATR
    atr = vbt.ATR.run(high=close, low=close, close=close, window=atr_length).atr
    atr_upper_bound = close + atr * atr_multiplier
    atr_lower_bound = close - atr * atr_multiplier

    # Long Entry Conditions
    long_entries = (close > bb.upper) & (rsi < rsi_upper) & (volume > vol_threshold)

    # Long Exit Conditions
    long_exits = (rsi > rsi_upper)

    # Short Entry Conditions
    short_entries = (close < bb.lower) & (rsi > rsi_lower) & (volume > vol_threshold)

    # Short Exit Conditions
    short_exits = (rsi < rsi_lower)

    return long_entries, long_exits, short_entries, short_exits, atr_upper_bound, atr_lower_bound, partial_tp_pct

def apply_stop_loss_take_profit(pf, atr_upper_bound, atr_lower_bound, partial_tp_pct):
    pf = pf.set_stop_loss(lambda x: np.where(x['Long'], atr_lower_bound[x.index], atr_upper_bound[x.index]))
    pf = pf.set_take_profit(lambda x: np.where(x['Long'], atr_upper_bound[x.index], atr_lower_bound[x.index]), 
                            tp_pct=partial_tp_pct)
    return pf
