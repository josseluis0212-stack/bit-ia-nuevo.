import logging
from core.bybit_client import BybitClient
from core.telegram_bot import TelegramBot
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Verifier")

def verify_connections():
    print("      VERIFICACIÓN DE CONEXIONES      ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    # 1. Check Bybit
    print("1. Conectando a Bybit...")
    try:
        bybit = BybitClient()
        price = bybit.get_market_price("BTCUSDT")
        if price:
            print(f"   [OK] Conexión Bybit exitosa. Precio BTC: {price}")
        else:
            print("   [ERROR] No se pudo obtener el precio de Bybit. Revisa tus llaves API.")
    except Exception as e:
        print(f"   [ERROR] Error en conexión Bybit: {e}")

    # 2. Check Telegram
    print("\n2. Conectando a Telegram...")
    try:
        bot = TelegramBot()
        res = bot.send_message("🔍 *Prueba de conexión del bot bit-ia-nuevo v3.0*")
        if res and res.get('ok'):
            print("   [OK] Mensaje de Telegram enviado con éxito.")
        else:
            print(f"   [ERROR] Fallo al enviar mensaje. Revisa TOKEN y CHAT_ID. (Respuesta: {res})")
    except Exception as e:
        print(f"   [ERROR] Error en conexión Telegram: {e}")

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Verificación finalizada.")

if __name__ == "__main__":
    verify_connections()
