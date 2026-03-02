import sys
import io
from pybit.unified_trading import HTTP

# Forzar UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_key(name, key, secret):
    print(f"Probando {name}...")
    session = HTTP(testnet=True, api_key=key, api_secret=secret)
    try:
        res = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
        print(f"✅ EXITO: {name}")
        return True
    except Exception as e:
        print(f"❌ FALLO: {name} - {e}")
        return False

def verify():
    keys = [
        ("VIR (Original)", "WFSXKPsVIRbYkhvFwn"),
        ("VlR (Con ele)", "WFSXKPsVlRbYkhvFwn"),
    ]
    
    # Variaciones del Secreto
    secrets = [
        ("Original (IYI3...)", "IYI3OahwX3mozGivmscqXPmr1430WaCNsgZW"),
        ("Con 'l' (IYl3...)", "IYl3OahwX3mozGivmscqXPmr1430WaCNsgZW"),
        ("Con '1' (1YI3...)", "1YI3OahwX3mozGivmscqXPmr1430WaCNsgZW"),
    ]
    
    for kn, key in keys:
        for sn, secret in secrets:
            if test_key(f"{kn} + {sn}", key, secret):
                print(f"\n¡ENCONTRADA!")
                print(f"KEY: {key}")
                print(f"SECRET: {secret}")
                return

if __name__ == "__main__":
    verify()
