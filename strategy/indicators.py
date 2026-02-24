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

def get_trend(klines_trend_main, klines_trend_sub):
    """
    Define la tendencia principal.
    Usuario solicita: EMA 50 en velas de una hora para tendencia.
    klines_trend_sub corresponde a 1h según config.
    """
    df_sub = pd.DataFrame(klines_trend_sub, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df_sub['close'] = df_sub['close'].astype(float)

    # EMA 50 en 1h (principal filtro de tendencia)
    ema50_1h = calculate_ema(df_sub['close'], 50)
    last_close_1h = df_sub['close'].iloc[-1]
    last_ema50_1h = ema50_1h.iloc[-1]

    # También revisamos el timeframe mayor (3h) para mayor seguridad
    df_main = pd.DataFrame(klines_trend_main, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df_main['close'] = df_main['close'].astype(float)
    ema50_3h = calculate_ema(df_main['close'], 50)
    
    trend_1h = "up" if last_close_1h > last_ema50_1h else "down"
    trend_3h = "up" if df_main['close'].iloc[-1] > ema50_3h.iloc[-1] else "down"

    if trend_1h == "up" and trend_3h == "up":
        return "long"
    elif trend_1h == "down" and trend_3h == "down":
        return "short"
    
    return "neutral"

def check_entry_signal(klines_entry):
    """
    Señal de entrada en 5m/15m:
    - EMA 8 cruza EMA 21
    """
    df = pd.DataFrame(klines_entry, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df['close'] = df['close'].astype(float)

    ema8  = calculate_ema(df['close'], 8)
    ema21 = calculate_ema(df['close'], 21)
    ema50 = calculate_ema(df['close'], 50)

    last_close = df['close'].iloc[-1]
    last_ema50 = ema50.iloc[-1]

    # Cruce alcista: ema8 cruza arriba de ema21 y precio > ema50 (en el TF de entrada)
    if ema8.iloc[-2] <= ema21.iloc[-2] and ema8.iloc[-1] > ema21.iloc[-1] and last_close > last_ema50:
        return "long"
    # Cruce bajista: ema8 cruza abajo de ema21 y precio < ema50 (en el TF de entrada)
    elif ema8.iloc[-2] >= ema21.iloc[-2] and ema8.iloc[-1] < ema21.iloc[-1] and last_close < last_ema50:
        return "short"

    return None
