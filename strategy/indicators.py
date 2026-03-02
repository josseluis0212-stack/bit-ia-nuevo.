import pandas as pd
import numpy as np
import config

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

def calculate_macd(prices, fast=12, slow=26, signal=9):
    exp1 = calculate_ema(prices, fast)
    exp2 = calculate_ema(prices, slow)
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    hist = macd - signal_line
    return macd, signal_line, hist

def calculate_bollinger_bands(prices, period=20, std_mult=2.0):
    sma = prices.rolling(period).mean()
    std = prices.rolling(period).std()
    upper = sma + std_mult * std
    lower = sma - std_mult * std
    return upper, sma, lower

def calculate_atr(high, low, close, period=14):
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(period).mean()

def get_trend(klines_trend_main, klines_trend_sub):
    """
    Tendencia Antigravity Alfa: Confluencia MA 200 e Histograma MACD
    """
    df_main = pd.DataFrame(klines_trend_main, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df_main['close'] = df_main['close'].astype(float)
    
    # EMA 200 Institutional
    ema200 = calculate_ema(df_main['close'], config.EMA_LONG_TERM)
    last_close = df_main['close'].iloc[-1]
    
    # MACD Trend
    _, _, hist = calculate_macd(df_main['close'])
    
    long_trend = last_close > ema200.iloc[-1] and hist.iloc[-1] > 0
    short_trend = last_close < ema200.iloc[-1] and hist.iloc[-1] < 0
    
    if long_trend: return "long"
    if short_trend: return "short"
    return "neutral"

def check_entry_signal(klines_entry):
    """
    Gatillo Antigravity Alfa: RSI + MACD Crossover en Timeframe de entrada
    """
    df = pd.DataFrame(klines_entry, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
    df['close'] = df['close'].astype(float)
    
    rsi = calculate_rsi(df['close'], config.RSI_PERIOD)
    macd, signal, hist = calculate_macd(df['close'], config.MACD_FAST, config.MACD_SLOW, config.MACD_SIGNAL)
    
    last_rsi = rsi.iloc[-1]
    last_hist = hist.iloc[-1]
    prev_hist = hist.iloc[-2]
    
    # Señal Long: MACD cruza a positivo + RSI no sobrecomprado
    if prev_hist <= 0 and last_hist > 0 and last_rsi < config.RSI_OVERBOUGHT:
        return "long"
        
    # Señal Short: MACD cruza a negativo + RSI no sobrevendido
    elif prev_hist >= 0 and last_hist < 0 and last_rsi > config.RSI_OVERSOLD:
        return "short"
        
    return None
