import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def graficar_frontera(datos_dict, n_simulaciones=5000):

    retornos_df = pd.DataFrame()

    for activo, datos in datos_dict.items():
        retornos_df[activo] = datos["Retorno"]

    retornos_df = retornos_df.dropna()

    mean_returns = retornos_df.mean() * 252
    cov_matrix = retornos_df.cov() * 252

    resultados = []

    mejor_sharpe = -999
    mejor_punto = (0, 0)

    # 🔁 TODO ESTO VA DENTRO DE LA FUNCIÓN
    for _ in range(n_simulaciones):
        pesos = np.random.random(len(mean_returns))
        pesos /= np.sum(pesos)

        retorno = np.dot(pesos, mean_returns)
        riesgo = np.sqrt(np.dot(pesos.T, np.dot(cov_matrix, pesos)))

        sharpe = retorno / riesgo if riesgo != 0 else 0

        resultados.append((riesgo, retorno))

        if sharpe > mejor_sharpe:
            mejor_sharpe = sharpe
            mejor_punto = (riesgo, retorno)

    riesgos = [r[0] for r in resultados]
    retornos = [r[1] for r in resultados]

    plt.figure(figsize=(10,6))
    plt.scatter(riesgos, retornos, alpha=0.3)

    # ⭐ punto óptimo
    plt.scatter(mejor_punto[0], mejor_punto[1], marker='*', s=300, label="Óptimo")

    plt.xlabel("Riesgo (Volatilidad)")
    plt.ylabel("Retorno Esperado")
    plt.title("Frontera Eficiente")
    plt.legend()
    plt.grid()

    plt.show()