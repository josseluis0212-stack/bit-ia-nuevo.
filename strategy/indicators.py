import pandas as pd
import numpy as np

def calculate_ema(prices, period):
    return prices.ewm(span=period, adjust=False).mean()

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_bollinger_bands(prices, period=20, std_mult=2.0):
    sma = prices.rolling(period).mean()
    std = prices.rolling(period).std()
    upper = sma + std_mult * std
    lower = sma - std_mult * std
    return upper, sma, lower

def calculate_atr(high, low, close, period=14):
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    tr = pd.concat([tr1, tr2, tr3], axis=1, join='inner').max(axis=1)
    return tr.rolling(period).mean()

def get_trend(klines_4h, klines_1h):
    """
    Define la tendencia principal usando EMA 50 en 4H + 1H.
    Retorna: 'long', 'short', o 'neutral'
    """
    df_4h = pd.DataFrame(klines_4h, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df_4h['close'] = df_4h['close'].astype(float)

    df_1h = pd.DataFrame(klines_1h, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df_1h['close'] = df_1h['close'].astype(float)

    ema50_4h = calculate_ema(df_4h['close'], 50)
    ema50_1h = calculate_ema(df_1h['close'], 50)

    trend_4h = "up" if df_4h['close'].iloc[-1] > ema50_4h.iloc[-1] else "down"
    trend_1h = "up" if df_1h['close'].iloc[-1] > ema50_1h.iloc[-1] else "down"

    if trend_4h == "up" and trend_1h == "up":
        return "long"
    elif trend_4h == "down" and trend_1h == "down":
        return "short"
    return "neutral"

def check_entry_signal(klines_5m):
    """
    Señal de entrada en 5m:
    - EMA 8 cruza EMA 21 al alza  -> LONG (precio sobre EMA 50)
    - EMA 8 cruza EMA 21 a la baja -> SHORT (precio bajo EMA 50)
    """
    df = pd.DataFrame(klines_5m, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df['close'] = df['close'].astype(float)
    df['vol'] = df['vol'].astype(float)

    ema8  = calculate_ema(df['close'], 8)
    ema21 = calculate_ema(df['close'], 21)
    ema50 = calculate_ema(df['close'], 50)

    last_close = df['close'].iloc[-1]
    last_ema50 = ema50.iloc[-1]

    # Cruce alcista: ema8 cruza arriba de ema21 y precio > ema50
    if ema8.iloc[-2] <= ema21.iloc[-2] and ema8.iloc[-1] > ema21.iloc[-1] and last_close > last_ema50:
        return "long"
    # Cruce bajista: ema8 cruza abajo de ema21 y precio < ema50
    elif ema8.iloc[-2] >= ema21.iloc[-2] and ema8.iloc[-1] < ema21.iloc[-1] and last_close < last_ema50:
        return "short"

    return None
