import numpy as np
import pandas as pd

def optimizar_portafolio_markowitz(datos_dict, n_simulaciones=5000):

    activos = list(datos_dict.keys())

    # Construir dataframe con retornos
    retornos_df = pd.DataFrame()

    for activo, datos in datos_dict.items():
        retornos_df[activo] = datos["Retorno"]

    retornos_df = retornos_df.dropna()

    mean_returns = retornos_df.mean() * 252
    cov_matrix = retornos_df.cov() * 252

    mejores = {
        "sharpe": -999,
        "pesos": None,
        "retorno": 0,
        "riesgo": 0
    }

    for _ in range(n_simulaciones):
        pesos = np.random.random(len(activos))
        pesos /= np.sum(pesos)

        retorno_port = np.dot(pesos, mean_returns)

        riesgo_port = np.sqrt(
            np.dot(pesos.T, np.dot(cov_matrix, pesos))
        )

        sharpe = retorno_port / riesgo_port if riesgo_port != 0 else 0

        if sharpe > mejores["sharpe"]:
            mejores = {
                "sharpe": sharpe,
                "pesos": pesos,
                "retorno": retorno_port,
                "riesgo": riesgo_port
            }

    return activos, mejores