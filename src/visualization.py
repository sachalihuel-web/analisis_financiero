import matplotlib.pyplot as plt
import os

def generar_grafico(datos, activo):
    datos["Retorno_Acumulado"].plot(title=f"Retorno acumulado - {activo}")

    ruta = os.path.join("reports", f"{activo}_grafico.png")

    plt.xlabel("Fecha")
    plt.ylabel("Crecimiento")
    plt.grid()

    plt.savefig(ruta)
    plt.close()

    return ruta