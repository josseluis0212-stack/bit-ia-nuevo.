import logging
import time
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import config
from core.bybit_client import BybitClient
from core.telegram_bot import TelegramBot
from core.stats_manager import StatsManager
from strategy.indicators import get_trend, check_entry_signal
from strategy.filter_engine import FilterEngine

import json
from strategy.indicators import get_trend, check_entry_signal, calculate_atr

# Global state for Web UI
GLOBAL_STATE = {
    "balance": 50000.0,
    "session_pnl": 0.0,
    "trend": "neutral",
    "open_trades": [],
    "logs": []
}

class WebHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.serve_file('web/index.html', 'text/html')
        elif self.path == '/styles.css':
            self.serve_file('web/styles.css', 'text/css')
        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(GLOBAL_STATE).encode())
        else:
            self.send_error(404)

    def serve_file(self, path, content_type):
        try:
            with open(path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404)

    def log_message(self, format, *args):
        return # Silence logging for health checks

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), WebHandler)
    server.serve_forever()

# Logging Custom Handler for Web UI
class WebLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        GLOBAL_STATE["logs"].insert(0, log_entry)
        if len(GLOBAL_STATE["logs"]) > 50:
            GLOBAL_STATE["logs"].pop()

# Logging Setup
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("MainLoop")
logger.addHandler(WebLogHandler())

class BotTrading:
    def __init__(self):
        self.bybit = BybitClient()
        self.telegram = TelegramBot()
        self.stats = StatsManager()
        self.filters = FilterEngine(self.bybit)
        self.last_report_date = datetime.utcnow().date()
        # Cargar TODOS los pares USDT Perpetuos dinamicamente
        self.symbol_list = self.bybit.get_all_usdt_symbols()
        logger.info(f"Antigravity Alfa v5.0 inicializado con {len(self.symbol_list)} pares")

    def run(self):
        # Start Web Server for UI
        threading.Thread(target=run_web_server, daemon=True).start()

        initial_balance = self.bybit.get_balance() or 0.0
        stats_now = self.stats.get_stats("day")

        self.telegram.send_message(
            f"🚀 *BIT-IA PRO v5.2: SISTEMA ACTIVADO*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 *Capital Inicia:* ${initial_balance:,.2f} USDT\n"
            f"📊 *Ops Hoy:* {stats_now['count']}   🎯 *Win Rate:* {stats_now['win_rate']}%\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🌐 *Escaneo:* TODOS los pares USDT Perpetuos\n"
            f"🧠 *IA Confianza:* {int(config.IA_PROBABILITY_THRESHOLD*100)}% (Alfa)\n"
            f"🛡️ *Filtros:* Volumen (+5M) | ATR Dinámico\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 _Bot operativo 24/7 en la Nube (Render)._"
        )

        while True:
            try:
                self.check_reports()
                self.track_closures()
                self.process_market()
                time.sleep(60) # Scan every minute
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(30)

    def track_closures(self):
        # We check the last 10 closed PnL records
        closed_trades = self.bybit.get_closed_pnl()
        for trade in closed_trades:
            order_id = trade['orderId']
            # Only process if we haven't recorded this orderId yet
            # For simplicity, we use a local cache or check against history
            if not any(t.get('order_id') == order_id for t in self.stats.history):
                symbol = trade['symbol']
                pnl = float(trade['closedPnl'])
                side = trade['side']
                entry_price = float(trade['avgEntryPrice'])
                exit_price = float(trade['avgExitPrice'])
                
                result = "GANANCIA" if pnl > 0 else "PERDIDA"
                
                # Save to stats
                self.stats.save_trade(symbol, side, entry_price, exit_price, 0.0, pnl, order_id)
                
                # Get updated stats for report
                current_stats = self.stats.get_stats("day")

                # Send Signal with stats
                self.telegram.send_closure_signal(symbol, side, pnl, result, stats=current_stats)
                
                # Autonomous Learning (Requirement 6/7)
                if result == "PERDIDA":
                    self.perform_autonomous_learning(trade)

    def perform_autonomous_learning(self, trade):
        # Basic autonomous adjustment: 
        # If we have 3 losses in the last 10 trades, increase filter sensitivity
        recent_losses = len([t for t in self.stats.history[-10:] if t.get('pnl_usd', 0) < 0])
        if recent_losses >= 3:
            logger.info("Autonomous Engine: Adjusting filters due to recent losses.")
            config.MIN_24H_VOLUME *= 1.1 # Be 10% more selective
            config.IA_PROBABILITY_THRESHOLD = min(0.85, config.IA_PROBABILITY_THRESHOLD + 0.02)
            self.telegram.send_message("🧠 *Ajuste Autónomo:* Se han incrementado los umbrales de seguridad tras detectar rachas negativas.")

    def process_market(self):
        open_count = self.bybit.get_open_positions_count()
        if open_count >= config.MAX_OPEN_TRADES:
            logger.info("Límite de operaciones alcanzado. Esperando cierres...")
            return

        for symbol in self.symbol_list:
            logger.info(f"Analizando {symbol} (Alfa v5.0)...")
            
            # Fetch Klines con temporalidades Alfa
            k_main = self.bybit.get_klines(symbol, config.TIMEFRAME_TREND_MAIN)
            k_entry = self.bybit.get_klines(symbol, config.TIMEFRAME_ENTRY)
            
            if not k_main or not k_entry:
                continue
                
            # Análisis de Tendencia Institucional (4H)
            trend = get_trend(k_main, k_main) # Usamos main para tendencia
            if trend == "neutral":
                continue
                
            # Señal de Gatillo (15m)
            entry_signal = check_entry_signal(k_entry)
            if entry_signal and entry_signal == trend:
                # Validar Filtros de Liquidez y Volatilidad
                passed, reason = self.filters.validate_filters(symbol, k_entry)
                if not passed:
                    logger.info(f"Señal rechazada: {reason}")
                    continue
                    
                # Calcular Probabilidad con Motor Alfa
                prob = self.filters.calculate_ia_probability(symbol, trend, entry_signal, k_entry)
                if prob < config.IA_PROBABILITY_THRESHOLD:
                    logger.info(f"Rechazado por Motor Alfa: {prob*100}% de confianza")
                    continue
                    
                # Gestión de Riesgo Dinámica (ATR)
                from strategy.indicators import calculate_atr
                df_entry = pd.DataFrame(k_entry, columns=['ts', 'open', 'high', 'low', 'close', 'vol', 'turnover'])
                df_entry['close'] = df_entry['close'].astype(float)
                df_entry['high'] = df_entry['high'].astype(float)
                df_entry['low'] = df_entry['low'].astype(float)
                
                atr = calculate_atr(df_entry['high'], df_entry['low'], df_entry['close']).iloc[-1]
                market_price = self.bybit.get_market_price(symbol)
                side = "Buy" if entry_signal == "long" else "Sell"
                
                if side == "Buy":
                    sl = round(market_price - (atr * config.ATR_SL_MULTIPLIER), 4)
                    tp = round(market_price + (atr * config.ATR_TP_MULTIPLIER), 4)
                else:
                    sl = round(market_price + (atr * config.ATR_SL_MULTIPLIER), 4)
                    tp = round(market_price - (atr * config.ATR_TP_MULTIPLIER), 4)
                
                # Cálculo de Tamaño de Posición ($100 de margen real con 5x)
                # Position Value = Qty * Price = Margin * Leverage
                qty = round((config.MARGIN_PER_TRADE * config.LEVERAGE) / market_price, 3)
                
                # Ejecución Autónoma
                order = self.bybit.open_position(symbol, side, qty, sl, tp)
                if order:
                    current_bal = self.bybit.get_balance()
                    self.telegram.send_signal(symbol, side, market_price, sl, tp, prob, balance=current_bal)
                    logger.info(f"Operación ABIERTA en {symbol} ({side})")
            
            time.sleep(0.5)
            
            # Update GLOBAL_STATE for Web UI
            self.update_web_state(symbol, trend)

    def update_web_state(self, symbol, trend):
        try:
            GLOBAL_STATE["balance"] = self.bybit.get_balance() or 50000.0
            GLOBAL_STATE["trend"] = trend
            total_pnl = sum([t.get('pnl_usd', 0) for t in self.stats.history])
            GLOBAL_STATE["session_pnl"] = total_pnl
            
            positions = self.bybit.session.get_positions(category="linear", settleCoin="USDT")['result']['list']
            GLOBAL_STATE["open_trades"] = [
                {
                    "symbol": p["symbol"],
                    "side": p["side"],
                    "entry_price": p["avgPrice"],
                    "pnl": float(p["unrealisedPnl"])
                } for p in positions if float(p["size"]) > 0
            ]
        except:
            pass

    def check_reports(self):
        now = datetime.utcnow()
        if now.date() > self.last_report_date:
            # Daily Report (Requirement 5 & 7)
            stats = self.stats.get_stats("day")
            chart = self.stats.generate_performance_chart()
            self.telegram.send_report("Diario", stats)
            # if chart:
            #     self.telegram.send_photo(chart, "Curva de Rendimiento Diaria")
            
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
