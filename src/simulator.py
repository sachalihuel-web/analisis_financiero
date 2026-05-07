def simular_inversion(mejor, capital_inicial=1000000):

    retorno = mejor["retorno"]
    riesgo = mejor["riesgo"]

    ganancia_esperada = capital_inicial * retorno
    valor_final = capital_inicial + ganancia_esperada

    perdida_potencial = capital_inicial * riesgo

    return {
        "capital_inicial": capital_inicial,
        "ganancia": ganancia_esperada,
        "valor_final": valor_final,
        "riesgo": perdida_potencial
    }