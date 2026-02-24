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
    
    # Requirement: Price alignment with EMA 50
    ema50_4h = calculate_ema(df_4h['close'], 50)
    ema50_1h = calculate_ema(df_1h['close'], 50)
    
    last_price_4h = df_4h['close'].iloc[-1]
    last_price_1h = df_1h['close'].iloc[-1]
    
    trend_4h = "up" if last_price_4h > ema50_4h.iloc[-1] else "down"
    trend_1h = "up" if last_price_1h > ema50_1h.iloc[-1] else "down"
    
    if trend_4h == "up" and trend_1h == "up":
        return "long"
    elif trend_4h == "down" and trend_1h == "down":
        return "short"
    return "neutral"

def check_entry_signal(klines_5m):
    df = pd.DataFrame(klines_5m, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df['close'] = df['close'].astype(float)
    
    ema8 = calculate_ema(df['close'], 8)
    ema20 = calculate_ema(df['close'], 20)
    ema50 = calculate_ema(df['close'], 50)
    
    # Crossover logic EMA 8 & 20
    last_ema8 = ema8.iloc[-1]
    last_ema20 = ema20.iloc[-1]
    last_ema50 = ema50.iloc[-1]
    prev_ema8 = ema8.iloc[-2]
    prev_ema20 = ema20.iloc[-2]
    
    # Requirement: Cross must be on the correct side of EMA 50
    if prev_ema8 <= prev_ema20 and last_ema8 > last_ema20 and df['close'].iloc[-1] > last_ema50:
        return "long"
    elif prev_ema8 >= prev_ema20 and last_ema8 < last_ema20 and df['close'].iloc[-1] < last_ema50:
        return "short"
    
    return None
