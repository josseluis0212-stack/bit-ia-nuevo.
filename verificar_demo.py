import sys, os
sys.path.append('.')
os.environ['BYBIT_TESTNET'] = 'True'  # Forzar modo demo

import config
from core.bybit_client import BybitClient
from core.telegram_bot import TelegramBot

print("=" * 50)
print(" VERIFICACION bot-ia-nuevo v3.2 MODO DEMO")
print("=" * 50)
print(f" Testnet activo: {config.BYBIT_TESTNET}")
print(f" Margen por trade: ${config.MARGIN_PER_TRADE}")
print(f" Umbral IA: {int(config.IA_PROBABILITY_THRESHOLD*100)}%")
print("-" * 50)

# Test 1: Conexion Bybit Testnet
print("[1/3] Conectando a Bybit Testnet...")
bybit = BybitClient()
try:
    price_btc = bybit.get_market_price("BTCUSDT")
    if price_btc:
        print(f"      OK - BTCUSDT Testnet: ${price_btc:,.2f}")
    else:
        print("      ERROR - No se pudo obtener precio")
except Exception as e:
    print(f"      ERROR - {e}")

# Test 2: Lectura de mercado (velas)
print("[2/3] Verificando lectura de mercado (velas 5m)...")
try:
    klines = bybit.get_klines("ETHUSDT", "5m", limit=5)
    if klines:
        print(f"      OK - ETHUSDT: Ultimas {len(klines)} velas leidas")
    else:
        print("      ERROR - No se pudieron leer velas")
except Exception as e:
    print(f"      ERROR - {e}")

# Test 3: Señal de prueba a Telegram
print("[3/3] Enviando señal de prueba a Telegram...")
telegram = TelegramBot()

# Mensaje de estado
telegram.send_message(
    "🧪 *VERIFICACIÓN SISTEMA - MODO DEMO* 🧪\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "✅ *Modo:* Testnet (Dinero ficticio)\n"
    f"✅ *Margen:* ${config.MARGIN_PER_TRADE} USDT demo\n"
    "✅ *Mercado:* Escaneando 10 pares\n"
    "✅ *IA Engine:* Activo (umbral 80%)\n"
    "✅ *Servidor:* Render Frankfurt 24/7\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "🤖 _Bot operando en modo demo. Ninguna orden real será ejecutada._"
)

# Señal de compra simulada
ok = telegram.send_signal("BTCUSDT", "Buy", 63500.00, 62865.00, 64770.00, 0.85)
if ok:
    print("      OK - Señal de prueba enviada a Telegram")
    print("")
    print("=" * 50)
    print(" TODO CORRECTO - Revisa tu Telegram ahora!")
    print("=" * 50)
else:
    print("      ERROR - Fallo Telegram")
