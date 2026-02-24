import requests
import logging
import config

class TelegramBot:
    def __init__(self):
        self.token = config.TELEGRAM_BOT_TOKEN
        self.chat_id = config.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.logger = logging.getLogger("TelegramBot")

    def send_message(self, text):
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": text, "parse_mode": "Markdown"}
            response = requests.post(url, json=payload)
            return response.json()
        except Exception as e:
            self.logger.error(f"Error sending Telegram message: {e}")
            return None

    def send_signal(self, symbol, side, entry_price, sl, tp, prob):
        emoji = "🚀" if side == "Buy" else "🔻"
        text = (
            f"{emoji} *NUEVA SEÑAL DETECTADA*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🪙 *Moneda:* {symbol}\n"
            f"↕️ *Dirección:* {side}\n"
            f"💰 *Monto:* ${config.MARGIN_PER_TRADE} (5x)\n"
            f"💵 *Precio Entrada:* {entry_price}\n"
            f"🛑 *SL:* {sl} | 🎯 *TP:* {tp}\n"
            f"🧠 *Probabilidad IA:* {int(prob*100)}%\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
        return self.send_message(text)

    def send_report(self, title, stats):
        # stats is a dict with WinRate, PnL, etc.
        text = (
            f"📊 *REPORTE DE RENDIMIENTO: {title}*\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"✅ *Win Rate:* {stats.get('win_rate', 0)}%\n"
            f"💰 *PnL Total:* ${stats.get('pnl', 0.0):.2f}\n"
            f"📉 *Max Drawdown:* {stats.get('max_dd', 0.0)}%\n"
            f"🔢 *Operaciones:* {stats.get('count', 0)}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
        return self.send_message(text)

    def send_photo(self, photo_path, caption=""):
        try:
            url = f"{self.base_url}/sendPhoto"
            files = {'photo': open(photo_path, 'rb')}
            payload = {'chat_id': self.chat_id, 'caption': caption}
            response = requests.post(url, data=payload, files=files)
            return response.json()
        except Exception as e:
            self.logger.error(f"Error sending Telegram photo: {e}")
            return None
