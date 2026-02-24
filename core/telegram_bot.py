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
        side_label = "COMPRA (Long) 🟢" if side == "Buy" else "VENTA (Short) 🔴"
        text = (
            f"⚡️ *BIT-IA PRO: SEÑAL DETECTADA*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💎 *Activo:* {symbol}\n"
            f"↕️ *Posición:* {side_label}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 *Monto:* ${config.MARGIN_PER_TRADE} USDT\n"
            f"⚙️ *Apalancamiento:* {config.LEVERAGE}x (Aislado)\n"
            f"💵 *Precio Entrada:* {entry_price}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 *Take Profit:* {tp} (+2%)\n"
            f"🛑 *Stop Loss:* {sl} (-1.5%)\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 *Confianza IA:* {int(prob*100)}%\n"
            f"⚠️ *Gestión:* Riesgo controlado activado.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )
        return self.send_message(text)

    def send_closure_signal(self, symbol, side, pnl_usd, result):
        emoji = "✨" if result == "GANANCIA" else "⚖️"
        res_color = "❇️ FINALIZADA CON ÉXITO" if result == "GANANCIA" else "⚠️ CIERRE POR RIESGO"
        text = (
            f"{emoji} *BIT-IA PRO: OPERACIÓN CERRADA*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🪙 *Moneda:* {symbol}\n"
            f"📈 *Estado:* {res_color}\n"
            f"📊 *Dirección:* {side}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 *PnL Neto:* {pnl_usd:+.2f} USDT\n"
            f"📅 *Win Rate objetivo:* {config.IA_PROBABILITY_THRESHOLD*100:.0f}%\n"
            f"━━━━━━━━━━━━━━━━━━━━━━"
        )
        return self.send_message(text)

    def send_period_report(self, period_label, stats):
        """
        Envía reporte de rendimiento para un periodo (Diario/Semanal/Mensual).
        stats = {"wins": int, "losses": int, "pnl": float, "best": str, "worst": str}
        """
        wins   = stats.get("wins", 0)
        losses = stats.get("losses", 0)
        total  = wins + losses
        pnl    = stats.get("pnl", 0.0)
        win_rate = (wins / total * 100) if total > 0 else 0.0
        best   = stats.get("best", "N/A")
        worst  = stats.get("worst", "N/A")

        # Barra visual de win rate (10 bloques)
        filled = int(win_rate / 10)
        bar = "🟩" * filled + "⬜" * (10 - filled)
        pnl_emoji = "📈" if pnl >= 0 else "📉"

        text = (
            f"📊 *REPORTE {period_label} — BIT-IA PRO*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ *Victorias:* {wins}   ❌ *Derrotas:* {losses}\n"
            f"📋 *Total Operaciones:* {total}\n"
            f"🎯 *Win Rate:* {win_rate:.1f}%\n"
            f"{bar}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{pnl_emoji} *PnL Neto:* {pnl:+.2f} USDT\n"
            f"🏆 *Mejor par:* {best}\n"
            f"⚠️ *Peor par:* {worst}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 _Análisis autónomo en curso. Siguiente revisión programada._"
        )
        return self.send_message(text)

    def send_report(self, title, stats):
        return self.send_period_report(title, stats)

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
