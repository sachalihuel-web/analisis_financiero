import yfinance as yf

def obtener_datos(activo, periodo="1y"):
    datos = yf.download(activo, period=periodo)
    return datos