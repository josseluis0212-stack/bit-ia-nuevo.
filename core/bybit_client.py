import logging
import time
from pybit.unified_trading import HTTP
import config

class BybitClient:
    def __init__(self):
        self.session = HTTP(
            testnet=config.BYBIT_TESTNET,
            api_key=config.BYBIT_API_KEY,
            api_secret=config.BYBIT_API_SECRET
        )
        self.logger = logging.getLogger("BybitClient")

    def set_leverage(self, symbol):
        try:
            # Forzamos modo de margen 'Aislado' y apalancamiento
            self.session.switch_margin_mode(
                category="linear",
                symbol=symbol,
                tradeMode=1, # 1=Isolated, 0=Cross
                buyLeverage=str(config.LEVERAGE),
                sellLeverage=str(config.LEVERAGE),
            )
            self.logger.info(f"Margen AISLADO y Apalancamiento {config.LEVERAGE}x aplicado a {symbol}")
        except Exception as e:
            if "not modified" in str(e).lower():
                self.logger.info(f"Apalancamiento {config.LEVERAGE}x ya configurado para {symbol}")
            else:
                try:
                    self.session.set_leverage(
                        category="linear",
                        symbol=symbol,
                        buyLeverage=str(config.LEVERAGE),
                        sellLeverage=str(config.LEVERAGE),
                    )
                    self.logger.info(f"Apalancamiento {config.LEVERAGE}x establecido para {symbol}")
                except Exception as e2:
                    self.logger.warning(f"No se pudo forzar el apalancamiento: {e2}")

    def get_market_price(self, symbol):
        try:
            tickers = self.session.get_tickers(category="linear", symbol=symbol)
            return float(tickers['result']['list'][0]['lastPrice'])
        except Exception as e:
            self.logger.error(f"Error getting market price for {symbol}: {e}")
            return None

    def open_position(self, symbol, side, qty, sl_price, tp_price):
        try:
            self.set_leverage(symbol)
            
            order = self.session.place_order(
                category="linear",
                symbol=symbol,
                side=side,
                orderType="Market",
                qty=str(qty),
                stopLoss=str(sl_price),
                takeProfit=str(tp_price),
                tpOrderType="Market",
                slOrderType="Market",
                positionIdx=0  # Unified/One-way
            )
            self.logger.info(f"Opened {side} position for {symbol}: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Failed to open position for {symbol}: {e}")
            return None

    def get_open_positions_count(self):
        try:
            positions = self.session.get_positions(category="linear", settleCoin="USDT")
            active_positions = [p for p in positions['result']['list'] if float(p['size']) > 0]
            return len(active_positions)
        except Exception as e:
            self.logger.error(f"Error checking open positions: {e}")
            return 0

    def get_all_usdt_symbols(self):
        """Obtiene dinámicamente todos los pares USDT Perpetuo activos de Bybit."""
        try:
            result = self.session.get_instruments_info(category="linear")
            symbols = [
                item['symbol'] for item in result['result']['list']
                if item['symbol'].endswith('USDT') and item['status'] == 'Trading'
            ]
            self.logger.info(f"Total de pares USDT Perpetuo encontrados: {len(symbols)}")
            return symbols
        except Exception as e:
            self.logger.error(f"Error obteniendo lista de pares: {e}")
            # Fallback a lista base si la API falla
            return ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ADAUSDT",
                    "XRPUSDT", "DOTUSDT", "LINKUSDT", "MATICUSDT", "AVAXUSDT"]

    def get_klines(self, symbol, interval, limit=100):
        try:
            # Map common intervals
            interval_map = {"5m": "5", "15m": "15", "1h": "60", "3h": "180", "4h": "240"}
            bybit_interval = interval_map.get(interval, interval)
            
            klines = self.session.get_kline(
                category="linear",
                symbol=symbol,
                interval=bybit_interval,
                limit=limit
            )
            return klines['result']['list']
        except Exception as e:
            self.logger.error(f"Error fetching klines for {symbol} ({interval}): {e}")
            return []

    def get_closed_pnl(self, symbol=None, limit=10):
        try:
            res = self.session.get_closed_pnl(
                category="linear",
                symbol=symbol,
                limit=limit
            )
            return res['result']['list']
        except Exception as e:
            self.logger.error(f"Error fetching closed PnL: {e}")
            return []

    def get_balance(self):
        try:
            res = self.session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
            balance = float(res['result']['list'][0]['coin'][0]['walletBalance'])
            return balance
        except Exception as e:
            self.logger.error(f"Error fetching balance: {e}")
            return None
