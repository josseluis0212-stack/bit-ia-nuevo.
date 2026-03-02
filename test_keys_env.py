import os
import sys
import io
from pybit.unified_trading import HTTP
from dotenv import load_dotenv

# Forzar UTF-8 para evitar errores en Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

def verify():
    key = os.getenv("BYBIT_API_KEY")
    secret = os.getenv("BYBIT_API_SECRET")
    
    print(f"Probando Llaves: {key[:5]}...")
    
    # Probar en Mainnet
    print("\n--- Probando en MAINNET ---")
    session_main = HTTP(testnet=False, api_key=key, api_secret=secret)
    try:
        res = session_main.get_wallet_balance(accountType="UNIFIED", coin="USDT")
        print("OK: CONECTADO A MAINNET (Cuenta Real)")
        print(f"Balance: {res['result']['list'][0]['coin'][0]['walletBalance']} USDT")
    except Exception as e:
        print(f"ERROR: FALLO EN MAINNET: {e}")

    # Probar en Testnet
    print("\n--- Probando en TESTNET ---")
    session_test = HTTP(testnet=True, api_key=key, api_secret=secret)
    try:
        res = session_test.get_wallet_balance(accountType="UNIFIED", coin="USDT")
        print("OK: CONECTADO A TESTNET (Cuenta Demo)")
        print(f"Balance: {res['result']['list'][0]['coin'][0]['walletBalance']} USDT")
    except Exception as e:
        print(f"ERROR: FALLO EN TESTNET: {e}")

if __name__ == "__main__":
    verify()
