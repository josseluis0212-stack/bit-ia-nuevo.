import pandas as pd
import numpy as np
import config
from strategy.indicators import calculate_atr

class FilterEngine:
    def __init__(self, bybit_client):
        self.bybit = bybit_client

    def validate_filters(self, symbol, klines_5m):
        # 1. Volume Check (24h)
        # Using a simplified check from klines for demo
        df = pd.DataFrame(klines_5m, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
        last_turnover = float(df['turnover'].iloc[-1]) # Approx 5m volume in USDT
        # Simplified: Check if currency is in our whitelist or meets a global volume if we had full ticker data
        # For now, we trust SYMBOL_LIST and check local volume spikes
        avg_turnover = df['turnover'].astype(float).mean()
        if last_turnover < (avg_turnover * 0.5): # Avoid dead candles
            return False, "Low volume"

        # 2. Volatility Check (ATR)
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        atr = calculate_atr(df['high'], df['low'], df['close'], 14)
        last_atr_pct = atr.iloc[-1] / df['close'].iloc[-1]
        
        if last_atr_pct < config.MIN_ATR_PCT:
            return False, "Low volatility"

        # 3. Macro Event (Placeholder for simplified manual/scheduled filter)
        # In a real setup, we'd check an Economic Calendar API
        # Here we block if it's top of the hour (common news time) inside a +- 2 min window
        from datetime import datetime
        now = datetime.utcnow()
        if now.minute in [59, 0, 1]:
            return False, "Macro time window guard"

        return True, "Filters passed"

    def calculate_ia_probability(self, symbol, trend, side, klines_5m):
        """
        IA v3.2: Hybrid Heuristic-Probabilistic Hybrid Model
        Threshold: 80% for execution.
        """
        df = pd.DataFrame(klines_5m, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
        df['close'] = df['close'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['vol'] = df['vol'].astype(float)
        
        score = 0.0
        
        # 1. Trend Alignment (30%)
        # Check if 5m trend matches macro trend and price is above/below EMA 50
        from strategy.indicators import calculate_ema
        ema50 = calculate_ema(df['close'], 50).iloc[-1]
        if trend == side:
            if (side == "long" and df['close'].iloc[-1] > ema50) or \
               (side == "short" and df['close'].iloc[-1] < ema50):
                score += 0.30
        
        # 2. Momentum & Volume Spike (30%)
        # Check recent volume relative to standard deviation
        avg_vol = df['vol'].rolling(20).mean().iloc[-1]
        std_vol = df['vol'].rolling(20).std().iloc[-1]
        last_vol = df['vol'].iloc[-1]
        
        if last_vol > (avg_vol + std_vol): # Significant spike
            score += 0.30
        elif last_vol > avg_vol:
            score += 0.15
            
        # 3. Mean Reversion Risk (Extension) (20%)
        # Avoid entries if price is too far from EMA 50 (over-extension)
        dist_to_ema = abs(df['close'].iloc[-1] - ema50) / ema50
        # If distance is > 1.5% from the mean, we subtract points or give 0
        if dist_to_ema < 0.015: 
            score += 0.20
        elif dist_to_ema < 0.025:
            score += 0.10
            
        # 4. Market Integrity (Volatility) (20%)
        atr = calculate_atr(df['high'], df['low'], df['close'], 14).iloc[-1]
        atr_pct = atr / df['close'].iloc[-1]
        
        if atr_pct > config.MIN_ATR_PCT:
            score += 0.20
        else:
            score += (atr_pct / config.MIN_ATR_PCT) * 0.20
            
        return round(score, 2)
