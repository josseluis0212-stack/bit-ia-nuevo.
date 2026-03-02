from pybit.unified_trading import HTTP

def check():
    session = HTTP(testnet=True, domain="bytick")
    # Intentamos ver a dónde apunta (aunque pybit oculta la url base en el objeto session usualmente)
    # Pero podemos sniffearla o ver si el error 401 viene de un sitio inexistente
    print(f"Sesion iniciada con testnet=True y domain='bytick'")
    try:
        session.get_tickers(category="linear", symbol="BTCUSDT")
    except Exception as e:
        print(f"Error detectado: {e}")

if __name__ == "__main__":
    check()
