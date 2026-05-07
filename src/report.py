import os

def generar_reporte(activo, retorno, volatilidad, ruta_grafico):
    if volatilidad < 0.15:
        riesgo = "BAJO"
    elif volatilidad < 0.30:
        riesgo = "MEDIO"
    else:
        riesgo = "ALTO"

    contenido = f"""
INFORME FINANCIERO - {activo}

Retorno: {retorno:.2%}
Volatilidad: {volatilidad:.2%}
Riesgo: {riesgo}

Gráfico generado en:
{ruta_grafico}

CONCLUSIÓN:
El activo presenta un nivel de riesgo {riesgo} con un retorno de {retorno:.2%}.
"""

    ruta = os.path.join("reports", f"informe_{activo}.txt")

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)

    return ruta, riesgo
    