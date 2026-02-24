import pandas as pd
import numpy as np
import config
from strategy.indicators import calculate_ema, calculate_rsi, calculate_bollinger_bands, calculate_atr
from datetime import datetime


class FilterEngine:
    def __init__(self, bybit_client):
        self.bybit = bybit_client

    def validate_filters(self, symbol, klines_5m):
        """
        Tres filtros previos antes de calcular probabilidad IA:
        1. Volumen adecuado
        2. Volatilidad mínima (no mercado muerto)
        3. Sin evento macro (top de hora)
        """
        df = pd.DataFrame(klines_5m, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
        df['close'] = df['close'].astype(float)
        df['high']  = df['high'].astype(float)
        df['low']   = df['low'].astype(float)
        df['vol']   = df['vol'].astype(float)
        df['turnover'] = df['turnover'].astype(float)

        # --- Filtro 1: Volumen adecuado ---
        avg_volume = df['turnover'].rolling(20).mean().iloc[-1]
        last_volume = df['turnover'].iloc[-1]
        if last_volume < avg_volume * 0.4:
            return False, "Volumen muy bajo"

        # --- Filtro 2: Volatilidad mínima (ATR) ---
        atr = calculate_atr(df['high'], df['low'], df['close'], 14)
        atr_pct = atr.iloc[-1] / df['close'].iloc[-1]
        if atr_pct < config.MIN_ATR_PCT:
            return False, "Volatilidad muy baja"

        # --- Filtro 3: Guardia macro (±2 min del top de hora) ---
        now = datetime.utcnow()
        if now.minute in [58, 59, 0, 1, 2]:
            return False, "Ventana evento macro"

        return True, "Filtros superados"

    def calculate_ia_probability(self, symbol, trend, side, klines_5m):
        """
        IA v4.0 - Probabilidad de alcanzar el TP del 2%.
        Fórmula ponderada basada en 4 pilares:
        - Alineación de tendencia (40%)
        - Calidad de la señal EMA (30%)
        - Volumen institucional (20%)
        - Estabilidad de volatilidad (10%)
        Umbral de ejecución: > 80%
        """
        df = pd.DataFrame(klines_5m, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
        df['close'] = df['close'].astype(float)
        df['high']  = df['high'].astype(float)
        df['low']   = df['low'].astype(float)
        df['vol']   = df['vol'].astype(float)

        score = 0.0
        close = df['close']

        ema8  = calculate_ema(close, 8)
        ema21 = calculate_ema(close, 21)
        ema50 = calculate_ema(close, 50)
        last_close = close.iloc[-1]

        # ------ PILAR 1: Alineación de tendencia (40%) ------
        # La tendencia macro (4H+1H) debe coincidir con el lado de entrada
        if trend == side:
            score += 0.25  # Tendencia confirmada
            # Bonus: precio sobre EMA 50 en 5m
            if (side == "long"  and last_close > ema50.iloc[-1]) or \
               (side == "short" and last_close < ema50.iloc[-1]):
                score += 0.15
        
        # ------ PILAR 2: Calidad de la señal EMA (30%) ------
        # Separación entre EMA 8 y EMA 21 (señal más fuerte si están separadas)
        ema_spread = abs(ema8.iloc[-1] - ema21.iloc[-1]) / last_close
        if ema_spread > 0.003:    # > 0.3% separación → señal fuerte
            score += 0.30
        elif ema_spread > 0.001:  # > 0.1% separación → señal moderada
            score += 0.15

        # ------ PILAR 3: Volumen institucional (20%) ------
        avg_vol = df['vol'].rolling(20).mean().iloc[-1]
        std_vol = df['vol'].rolling(20).std().iloc[-1]
        last_vol = df['vol'].iloc[-1]

        if last_vol > (avg_vol + std_vol):  # Pico significativo
            score += 0.20
        elif last_vol > avg_vol:
            score += 0.10

        # ------ PILAR 4: Espacio libre hasta TP (10%) ------
        # Verifica si el precio no está demasiado extendido
        dist_to_ema50 = abs(last_close - ema50.iloc[-1]) / last_close
        if dist_to_ema50 < 0.01:    # Cerca de EMA 50 → buena probabilidad de expansión
            score += 0.10
        elif dist_to_ema50 < 0.02:
            score += 0.05

        return round(min(score, 1.0), 2)
