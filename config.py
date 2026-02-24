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
SYMBOL_LIST = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT", "DOTUSDT", "LINKUSDT", "MATICUSDT", "AVAXUSDT"]
MARGIN_PER_TRADE = 100.0  # USD (Stakes increased for v3.2)
LEVERAGE = 5
MAX_OPEN_TRADES = 10

# Strategy Parameters
TIMEFRAME_TREND_MAIN = "4h"
TIMEFRAME_TREND_SUB = "1h"
TIMEFRAME_ENTRY = "5m"
EMA_FAST = 8
EMA_MID = 21
EMA_SLOW = 50

# Risk Management
STOP_LOSS_PCT = 0.015  # 1.5%
TAKE_PROFIT_PCT = 0.02  # 2%
MAX_DAILY_DRAWDOWN = 0.05  # 5% target to stop bot

# Filter Thresholds
MIN_24H_VOLUME = 10000000  # 10M USDT
MIN_ATR_PCT = 0.003        # 0.3% volatility
IA_PROBABILITY_THRESHOLD = 0.80  # Professional Threshold increased to 80%
