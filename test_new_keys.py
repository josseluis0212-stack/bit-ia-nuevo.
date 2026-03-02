import sys
import io
from pybit.unified_trading import HTTP

# Forzar UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def verify():
    key = "WFSXKPsVIRbYkhvFwn"
    secret = "IYl3OahwX3mozGivmscqXPmr1430WaCNsgZW"
    
    print(f"Probando Llaves Nuevas: {key[:5]}...")
    
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
