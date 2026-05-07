import pandas as pd

def calcular_metricas(datos):
    datos["Retorno"] = datos["Close"].pct_change()
    datos["Retorno_Acumulado"] = (1 + datos["Retorno"]).cumprod()

    retorno_total = datos["Retorno_Acumulado"].iloc[-1] - 1
    volatilidad = datos["Retorno"].std() * (252 ** 0.5)

    score = retorno_total / volatilidad if volatilidad != 0 else 0
    return retorno_total, volatilidad, score, datos 