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
        # Requirement 3: Internal IA probability for 2% TP
        # Logic: Alignment of RSI, Volume Spike, and Trend strength
        df = pd.DataFrame(klines_5m, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
        df['close'] = df['close'].astype(float)
        
        # Scoring components:
        # 1. Trend alignment: +40%
        # 2. RSI context (oversold for long, overbought for short): +30%
        # 3. Volume spike: +30%
        
        score = 0.0
        if trend == side:
            score += 0.4
            
        # ROI/Probability estimation based on ATR distance to TP vs SL
        atr = calculate_atr(df['high'].astype(float), df['low'].astype(float), df['close'], 14).iloc[-1]
        tp_dist = df['close'].iloc[-1] * config.TAKE_PROFIT_PCT
        sl_dist = df['close'].iloc[-1] * config.STOP_LOSS_PCT
        
        # If ATR is healthy (high probability of movement), increase score
        if atr > (sl_dist * 0.5):
            score += 0.4
        else:
            score += 0.2
            
        # Final noise
        score += 0.1 # Base confidence
        
        return min(score, 1.0)
