import streamlit as st
import pandas as pd

from src.data_loader import obtener_datos
from src.analysis import calcular_metricas
from src.optimizer import optimizar_portafolio_markowitz
from src.simulator import simular_inversion

st.set_page_config(page_title="Analizador Financiero", layout="wide")

st.title("🏦 Plataforma de Análisis de Inversiones")
st.caption("Sistema cuantitativo de optimización de portafolios")

# 🔹 Sidebar
st.sidebar.header("Configuración")

activos = st.sidebar.multiselect(
    "Selecciona activos",
    ["SPY", "AAPL", "MSFT", "TSLA"],
    default=["SPY", "AAPL", "MSFT", "TSLA"]
)

capital = st.sidebar.number_input(
    "Capital inicial ($)",
    min_value=100000,
    value=1000000,
    step=100000
)

if st.sidebar.button("Analizar"):

    resultados = []
    datos_dict = {}

    # 🔁 Obtener datos
    for activo in activos:
        datos = obtener_datos(activo)

        retorno, volatilidad, score, datos = calcular_metricas(datos)

        datos_dict[activo] = datos

        resultados.append({
            "activo": activo,
            "retorno": retorno,
            "volatilidad": volatilidad,
            "score": score
        })

    # 🏆 Ranking
    ranking = sorted(resultados, key=lambda x: x["score"], reverse=True)

    df_ranking = pd.DataFrame(ranking)

    df_ranking["retorno"] = df_ranking["retorno"].map(
        lambda x: f"{x:.2%}"
    )

    df_ranking["volatilidad"] = df_ranking["volatilidad"].map(
        lambda x: f"{x:.2%}"
    )

    df_ranking["score"] = df_ranking["score"].map(
        lambda x: f"{x:.2f}"
    )

    st.subheader("🏆 Ranking de Activos")
    st.dataframe(df_ranking, use_container_width=True)

    # 🏦 Optimización
    activos_opt, mejor = optimizar_portafolio_markowitz(datos_dict)

    st.subheader("🏦 Portafolio Óptimo")

    for activo, peso in zip(activos_opt, mejor["pesos"]):
        st.write(f"{activo} → {peso:.2%}")

    # 📊 Gráfico
    df_pesos = pd.DataFrame({
        "Activo": activos_opt,
        "Peso": mejor["pesos"]
    })

    st.subheader("📊 Distribución del Portafolio")

    chart_data = df_pesos.set_index("Activo")

    st.bar_chart(chart_data, use_container_width=True)

    # 📈 Métricas
    st.write(f"📈 Retorno esperado: {mejor['retorno']:.2%}")
    st.write(f"⚠️ Riesgo: {mejor['riesgo']:.2%}")
    st.write(f"🏆 Sharpe: {mejor['sharpe']:.2f}")

    # 🚦 Riesgo visual
    if mejor["riesgo"] < 0.15:
        st.success("✅ Riesgo controlado")

    elif mejor["riesgo"] < 0.30:
        st.warning("⚠️ Riesgo moderado")

    else:
        st.error("🚨 Riesgo elevado")

    # 🧠 Recomendación
    mejor_activo = ranking[0]["activo"]

    st.subheader("🧠 Recomendación")

    st.info(
        f"El modelo sugiere mayor exposición a {mejor_activo} "
        f"por su mejor relación retorno/riesgo."
    )

    # 💰 Simulación
    sim = simular_inversion(mejor, capital)

    st.subheader("💰 Simulación")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Capital",
        f"${sim['capital_inicial']:,.0f}"
    )

    col2.metric(
        "📈 Ganancia",
        f"${sim['ganancia']:,.0f}"
    )

    col3.metric(
        "⚠️ Riesgo",
        f"${sim['riesgo']:,.0f}"
    )