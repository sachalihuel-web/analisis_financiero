from src.data_loader import obtener_datos
from src.analysis import calcular_metricas
from src.report import generar_reporte
from src.visualization import generar_grafico
from src.export_word import exportar_word
from src.portfolio import calcular_portafolio
from src.optimizer import optimizar_portafolio_markowitz
from src.efficient_frontier import graficar_frontera
from src.simulator import simular_inversion

activos = ["SPY", "AAPL", "MSFT", "TSLA"]

resultados = []
datos_dict = {}

# 🔁 LOOP PRINCIPAL
for activo in activos:
    datos = obtener_datos(activo)

    retorno, volatilidad, score, datos = calcular_metricas(datos)

    datos_dict[activo] = datos

    ruta_grafico = generar_grafico(datos, activo)
    ruta_reporte, riesgo = generar_reporte(activo, retorno, volatilidad, ruta_grafico)
    ruta_word = exportar_word(activo, retorno, volatilidad, riesgo, ruta_grafico)

    resultados.append({
        "activo": activo,
        "retorno": retorno,
        "volatilidad": volatilidad,
        "score": score,
        "riesgo": riesgo
    })

print("✅ Análisis completado")

# 🏆 RANKING
ranking = sorted(resultados, key=lambda x: x["score"], reverse=True)

print("\n🏆 RANKING PROFESIONAL:")
for i, r in enumerate(ranking, 1):
    print(f"{i}. {r['activo']} | Score: {r['score']:.2f} | Retorno: {r['retorno']:.2%} | Riesgo: {r['riesgo']}")

# 💼 PORTAFOLIO SIMPLE
portafolio = calcular_portafolio(resultados)

print("\n💼 PORTAFOLIO SUGERIDO:")
for p in portafolio:
    print(f"{p['activo']} → {p['peso']:.2%} | Riesgo: {p['riesgo']}")

# 🏦 MARKOWITZ
activos_opt, mejor = optimizar_portafolio_markowitz(datos_dict)

print("\n🏦 PORTAFOLIO ÓPTIMO (MARKOWITZ):")
for activo, peso in zip(activos_opt, mejor["pesos"]):
    print(f"{activo} → {peso:.2%}")

print(f"\n📈 Retorno esperado: {mejor['retorno']:.2%}")
print(f"⚠️ Riesgo: {mejor['riesgo']:.2%}")
print(f"🏆 Sharpe: {mejor['sharpe']:.2f}")

# 💰 SIMULACIÓN (UNA SOLA VEZ)
sim = simular_inversion(mejor, capital_inicial=1000000)

print("\n💰 SIMULACIÓN DE INVERSIÓN:")
print(f"Capital inicial: ${sim['capital_inicial']:,}")
print(f"Ganancia esperada: ${sim['ganancia']:,}")
print(f"Valor final estimado: ${sim['valor_final']:,}")
print(f"⚠️ Riesgo (posible pérdida): ${sim['riesgo']:,}")

# 📊 GRÁFICO FINAL
graficar_frontera(datos_dict)
