import pandas as pd
import numpy as np
import config
from strategy.indicators import calculate_ema, calculate_rsi, calculate_bollinger_bands, calculate_atr, calculate_macd
from datetime import datetime

class FilterEngine:
    def __init__(self, bybit_client):
        self.bybit = bybit_client

    def validate_filters(self, symbol, klines_entry):
        """
        Filtros de seguridad profesional v5.0:
        1. Liquidez (Volumen Relativo)
        2. Volatilidad (BB Width)
        3. Evitar Eventos Macro (Top de hora)
        """
        df = pd.DataFrame(klines_entry, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
        df['close'] = df['close'].astype(float)
        df['vol'] = df['vol'].astype(float)
        df['turnover'] = df['turnover'].astype(float)

        # --- Filtro 1: Liquidez (Volumen 24h y Relativo) ---
        # El volumen debe ser al menos 1.5x el promedio de las últimas 20 velas
        avg_vol = df['vol'].rolling(20).mean().iloc[-1]
        last_vol = df['vol'].iloc[-1]
        if last_vol < avg_vol * 1.2:
            return False, "Baja presión de volumen relativo"

        # --- Filtro 2: Volatilidad (Bollinger Band Width) ---
        upper, sma, lower = calculate_bollinger_bands(df['close'], 20)
        bb_width = (upper.iloc[-1] - lower.iloc[-1]) / sma.iloc[-1]
        if bb_width < 0.005:  # Menos del 0.5% de ancho = Mercado lateral/muerto
            return False, "Mercado en compresión lateral (muerto)"

        # --- Filtro 3: Ventana Macro ---
        now = datetime.utcnow()
        if now.minute in [59, 0, 1]:  # Reducido a ±1 min para ser más eficiente
            return False, "Protección volatilidad de cambio de hora"

        return True, "Filtros Alfa superados"

    def calculate_ia_probability(self, symbol, trend, side, klines_entry):
        """
        Motor Probabilístico Antigravity Alfa (0-100%).
        Confluencia de 4 Pilares:
        - Soporte de Tendencia (EMA 200 + Macro) (30%)
        - Fuerza del Momento (MACD + RSI) (30%)
        - Confirmación de Volatilidad (BB Position) (20%)
        - Calidad del Volumen (VSA Básico) (20%)
        """
        df = pd.DataFrame(klines_entry, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
        df['close'] = df['close'].astype(float)
        df['vol'] = df['vol'].astype(float)
        
        score = 0.0
        last_close = df['close'].iloc[-1]
        
        # 1. Pilar Tendencia (30%)
        ema200 = calculate_ema(df['close'], config.EMA_LONG_TERM).iloc[-1]
        if trend == side:
            score += 0.20
            # Bonus si estamos a favor de la tendencia institucional
            if (side == "long" and last_close > ema200) or (side == "short" and last_close < ema200):
                score += 0.10

        # 2. Pilar Momento (30%)
        macd, signal, hist = calculate_macd(df['close'])
        rsi = calculate_rsi(df['close']).iloc[-1]
        
        # MACD Histograma en aumento/disminución a favor
        if (side == "long" and hist.iloc[-1] > hist.iloc[-2]) or \
           (side == "short" and hist.iloc[-1] < hist.iloc[-2]):
            score += 0.15
            
        # RSI en zona óptima (no extremo)
        if (side == "long" and 40 < rsi < 65) or (side == "short" and 35 < rsi < 60):
            score += 0.15

        # 3. Pilar Volatilidad (20%)
        upper, sma, lower = calculate_bollinger_bands(df['close'])
        # Estamos cerca de la media pero con dirección?
        dist_to_sma = abs(last_close - sma.iloc[-1]) / last_close
        if dist_to_sma < 0.01: # Cercanía saludable para continuar movimiento
            score += 0.20

        # 4. Pilar Volumen (20%)
        avg_vol = df['vol'].rolling(20).mean().iloc[-1]
        if df['vol'].iloc[-1] > avg_vol:
            score += 0.20

        return round(score, 2)
