def calcular_portafolio(resultados):
    total_score = sum(r["score"] for r in resultados if r["score"] > 0)

    portafolio = []

    for r in resultados:
        if total_score > 0:
            peso = r["score"] / total_score
        else:
            peso = 0

        portafolio.append({
            "activo": r["activo"],
            "peso": peso,
            "retorno": r["retorno"],
            "riesgo": r["riesgo"]
        })

    return portafolio