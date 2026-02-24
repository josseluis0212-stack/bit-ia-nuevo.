import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.curdir))

from core.telegram_bot import TelegramBot
import config

def send_test_signal():
    bot = TelegramBot()
    print("Enviando señal de prueba Pro v3.2...")
    
    # Simular una señal de compra de alta confianza
    symbol = "BTCUSDT"
    side = "Buy"
    entry = 65432.10
    sl = 64777.77
    tp = 66740.74
    prob = 0.89 # 89% Confianza IA
    
    success = bot.send_signal(symbol, side, entry, sl, tp, prob)
    
    if success:
        print("✅ Señal de prueba enviada con éxito. Revisa tu Telegram.")
        # También enviar un mensaje de cierre simulado para probar la estética de ganancias
        bot.send_closure_signal(symbol, "LONG", 12.50, "GANANCIA")
    else:
        print("❌ Error al enviar la señal. Revisa tu token y chat_id en el archivo .env")

if __name__ == "__main__":
    send_test_signal()
