import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET", "")
BYBIT_TESTNET = os.getenv("BYBIT_TESTNET", "True").lower() == "true"  # Demo por defecto
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Trading Parameters
SYMBOL_LIST = []  # Se llenará dinámicamente en main.py (escaneo total)
MARGIN_PER_TRADE = 100.0  # $100 USDT de margen por operación
LEVERAGE = 5              # Apalancamiento fijo 5x
MAX_OPEN_TRADES = 10
BYBIT_TESTNET = True # MODO DEMO SIEMPRE ACTIVO

# Strategy Parameters (Antigravity Alfa v5.0)
TIMEFRAME_TREND_MAIN = "4h"   # Tendencia macro
TIMEFRAME_TREND_SUB = "1h"    # Tendencia intermedia
TIMEFRAME_ENTRY = "15m"       # Gatillo de entrada mejorado (menos ruido que 5m)

# Indicadores Técnicos
EMA_LONG_TERM = 200           # Filtro de tendencia institucional
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Risk Management Dinámico (ATR)
ATR_PERIOD = 14
ATR_SL_MULTIPLIER = 1.5       # Stop Loss dinámico basado en volatilidad
ATR_TP_MULTIPLIER = 2.5       # Take Profit dinámico (Ratio Riesgo:Beneficio > 1:1.5)

# Filter Thresholds
IA_PROBABILITY_THRESHOLD = 0.85  # Umbral de alta confianza Alfa
MIN_24H_VOLUME = 5000000        # 5M USDT volumen mínimo para liquidez
