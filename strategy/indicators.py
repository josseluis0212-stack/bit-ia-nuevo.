import pandas as pd
import numpy as np

def calculate_ema(prices, period):
    return prices.ewm(span=period, adjust=False).mean()

def calculate_atr(high, low, close, period=14):
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis=1, join='inner').max(axis=1)
    atr = tr.rolling(period).mean()
    return atr

def get_trend(klines_4h, klines_1h):
    # Convert Bybit klines to DataFrame
    df_4h = pd.DataFrame(klines_4h, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df_4h['close'] = df_4h['close'].astype(float)
    
    df_1h = pd.DataFrame(klines_1h, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df_1h['close'] = df_1h['close'].astype(float)
    
    # Simple trend detection: Slope of EMA 21 on 4H and 1H
    ema21_4h = calculate_ema(df_4h['close'], 21)
    ema21_1h = calculate_ema(df_1h['close'], 21)
    
    trend_4h = "up" if ema21_4h.iloc[-1] > ema21_4h.iloc[-2] else "down"
    trend_1h = "up" if ema21_1h.iloc[-1] > ema21_1h.iloc[-2] else "down"
    
    if trend_4h == "up" and trend_1h == "up":
        return "long"
    elif trend_4h == "down" and trend_1h == "down":
        return "short"
    return "neutral"

def check_entry_signal(klines_5m):
    df = pd.DataFrame(klines_5m, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df['close'] = df['close'].astype(float)
    
    ema8 = calculate_ema(df['close'], 8)
    ema21 = calculate_ema(df['close'], 21)
    
    # Crossover logic
    last_ema8 = ema8.iloc[-1]
    last_ema21 = ema21.iloc[-1]
    prev_ema8 = ema8.iloc[-2]
    prev_ema21 = ema21.iloc[-2]
    
    if prev_ema8 <= prev_ema21 and last_ema8 > last_ema21:
        return "long"
    elif prev_ema8 >= prev_ema21 and last_ema8 < last_ema21:
        return "short"
    
    return None
