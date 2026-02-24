import logging
import time
from datetime import datetime
import config
from core.bybit_client import BybitClient
from core.telegram_bot import TelegramBot
from core.stats_manager import StatsManager
from strategy.indicators import get_trend, check_entry_signal
from strategy.filter_engine import FilterEngine

# Logging Setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("MainLoop")

class BotTrading:
    def __init__(self):
        self.bybit = BybitClient()
        self.telegram = TelegramBot()
        self.stats = StatsManager()
        self.filters = FilterEngine(self.bybit)
        self.last_report_date = datetime.utcnow().date()
        logger.info("Bot bit-ia-nuevo v3.0 initialized")

    def run(self):
        self.telegram.send_message("🚀 *Bot bit-ia-nuevo v3.0 OPERATIVO*\nEl sistema está analizando el mercado 24/7.")
        
        while True:
            try:
                self.check_reports()
                self.process_market()
                time.sleep(60) # Scan every minute
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(30)

    def process_market(self):
        open_count = self.bybit.get_open_positions_count()
        if open_count >= config.MAX_OPEN_TRADES:
            logger.info("Max open trades reached. Skipping scan.")
            return

        for symbol in config.SYMBOL_LIST:
            logger.info(f"Analyzing {symbol}...")
            
            # Fetch Klines
            k_4h = self.bybit.get_klines(symbol, "4h")
            k_1h = self.bybit.get_klines(symbol, "1h")
            k_5m = self.bybit.get_klines(symbol, "5m")
            
            if not k_4h or not k_1h or not k_5m:
                continue
                
            # MTF Trend Analysis (Requirement 2)
            trend = get_trend(k_4h, k_1h)
            if trend == "neutral":
                continue
                
            # Entry Signal on 5m (Requirement 2)
            entry_signal = check_entry_signal(k_5m)
            if entry_signal and entry_signal == trend:
                # Valid Signal Found
                logger.info(f"Potential signal for {symbol}: {entry_signal}")
                
                # Filters (Requirement 3)
                passed, reason = self.filters.validate_filters(symbol, k_5m)
                if not passed:
                    logger.info(f"Signal rejected: {reason}")
                    continue
                    
                # IA Probability (Requirement 3)
                prob = self.filters.calculate_ia_probability(symbol, trend, entry_signal, k_5m)
                if prob < config.IA_PROBABILITY_THRESHOLD:
                    logger.info(f"Signal rejected by IA: {prob*100}% probability")
                    continue
                    
                # Calculate Prices (Requirement 6)
                market_price = self.bybit.get_market_price(symbol)
                side = "Buy" if entry_signal == "long" else "Sell"
                
                if side == "Buy":
                    sl = round(market_price * (1 - config.STOP_LOSS_PCT), 4)
                    tp = round(market_price * (1 + config.TAKE_PROFIT_PCT), 4)
                else:
                    sl = round(market_price * (1 + config.STOP_LOSS_PCT), 4)
                    tp = round(market_price * (1 - config.TAKE_PROFIT_PCT), 4)
                
                qty = round(config.MARGIN_PER_TRADE * config.LEVERAGE / market_price, 3)
                
                # Open Position (Requirement 1 & 4)
                order = self.bybit.open_position(symbol, side, qty, sl, tp)
                if order:
                    self.telegram.send_signal(symbol, side, market_price, sl, tp, prob)
                    # For tracking, we record the entry. Closure tracking would require a more complex loop or webhooks.
                    # Simplified for this build:
                    logger.info(f"Position opened for {symbol}")

    def check_reports(self):
        now = datetime.utcnow()
        if now.date() > self.last_report_date:
            # Daily Report (Requirement 5 & 7)
            stats = self.stats.get_stats("day")
            chart = self.stats.generate_performance_chart()
            self.telegram.send_report("Diario", stats)
            if chart:
                self.telegram.send_photo(chart, "Curva de Rendimiento Diaria")
            
            # Weekly check
            if now.weekday() == 0: # Monday
                stats_w = self.stats.get_stats("week")
                self.telegram.send_report("Semanal", stats_w)
                
            # Monthly check
            if now.day == 1:
                stats_m = self.stats.get_stats("month")
                self.telegram.send_report("Mensual", stats_m)
                
            self.last_report_date = now.date()

if __name__ == "__main__":
    bot = BotTrading()
    bot.run()
