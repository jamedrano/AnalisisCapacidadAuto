import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Modelo Monte Carlo - Capacidad Reclamos", layout="wide")

st.title("Modelo de Simulación Monte Carlo")
st.subheader("Capacidad Operativa - Reclamos Automóviles")

# =========================
# SIDEBAR INPUTS
# =========================

st.sidebar.header("Parámetros de Demanda")

avg_demand = st.sidebar.number_input("Demanda promedio mensual", value=7500)
std_demand = st.sidebar.number_input("Desviación estándar demanda", value=800)

st.sidebar.header("FTE Disponibles")

analyst_fte = st.sidebar.number_input("FTE Analistas", value=15)
adjuster_fte = st.sidebar.number_input("FTE Ajustadores", value=3)
registration_fte = st.sidebar.number_input("FTE Registro", value=3)

hours_per_fte = st.sidebar.number_input("Horas disponibles por FTE/mes", value=176)

st.sidebar.header("Tiempo promedio por orden (horas)")

analyst_time_mean = st.sidebar.number_input("Analistas - promedio", value=0.30)
analyst_time_std = st.sidebar.number_input("Analistas - desviación", value=0.05)

adjuster_time_mean = st.sidebar.number_input("Ajustadores - promedio", value=0.20)
adjuster_time_std = st.sidebar.number_input("Ajustadores - desviación", value=0.04)

registration_time_mean = st.sidebar.number_input("Registro - promedio", value=0.08)
registration_time_std = st.sidebar.number_input("Registro - desviación", value=0.02)

iterations = st.sidebar.slider("Número de iteraciones", 500, 10000, 2000)

run_sim = st.sidebar.button("Ejecutar Simulación")

# =========================
# MONTE CARLO
# =========================

if run_sim:

    np.random.seed()

    demand = np.random.normal(avg_demand, std_demand, iterations)
    demand = np.maximum(demand, 0)

    analyst_time = np.random.normal(analyst_time_mean, analyst_time_std, iterations)
    adjuster_time = np.random.normal(adjuster_time_mean, adjuster_time_std, iterations)
    registration_time = np.random.normal(registration_time_mean, registration_time_std, iterations)

    analyst_hours_required = demand * analyst_time
    adjuster_hours_required = demand * adjuster_time
    registration_hours_required = demand * registration_time

    analyst_capacity = analyst_fte * hours_per_fte
    adjuster_capacity = adjuster_fte * hours_per_fte
    registration_capacity = registration_fte * hours_per_fte

    analyst_gap = analyst_hours_required - analyst_capacity
    adjuster_gap = adjuster_hours_required - adjuster_capacity
    registration_gap = registration_hours_required - registration_capacity

    # =========================
    # RESULTADOS NUMÉRICOS
    # =========================

    st.header("Resultados Clave")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Analistas")
        st.write("Probabilidad de saturación:",
                 np.mean(analyst_gap > 0))
        st.write("Utilización promedio:",
                 np.mean(analyst_hours_required / analyst_capacity))
        st.write("FTE requeridos P95:",
                 np.percentile(analyst_hours_required, 95) / hours_per_fte)

    with col2:
        st.subheader("Ajustadores")
        st.write("Probabilidad de saturación:",
                 np.mean(adjuster_gap > 0))
        st.write("Utilización promedio:",
                 np.mean(adjuster_hours_required / adjuster_capacity))
        st.write("FTE requeridos P95:",
                 np.percentile(adjuster_hours_required, 95) / hours_per_fte)

    with col3:
        st.subheader("Registro")
        st.write("Probabilidad de saturación:",
                 np.mean(registration_gap > 0))
        st.write("Utilización promedio:",
                 np.mean(registration_hours_required / registration_capacity))
        st.write("FTE requeridos P95:",
                 np.percentile(registration_hours_required, 95) / hours_per_fte)

    # =========================
    # GRÁFICOS
    # =========================

    st.header("Distribuciones")

    # Demanda
    fig1 = plt.figure()
    plt.hist(demand, bins=40)
    plt.title("Distribución de Demanda")
    st.pyplot(fig1)

    # Analistas
    fig2 = plt.figure()
    plt.hist(analyst_hours_required, bins=40)
    plt.axvline(analyst_capacity)
    plt.title("Horas Requeridas - Analistas")
    st.pyplot(fig2)

    # Ajustadores
    fig3 = plt.figure()
    plt.hist(adjuster_hours_required, bins=40)
    plt.axvline(adjuster_capacity)
    plt.title("Horas Requeridas - Ajustadores")
    st.pyplot(fig3)

    # Registro
    fig4 = plt.figure()
    plt.hist(registration_hours_required, bins=40)
    plt.axvline(registration_capacity)
    plt.title("Horas Requeridas - Registro")
    st.pyplot(fig4)

    # =========================
    # DATAFRAME DESCARGABLE
    # =========================

    results_df = pd.DataFrame({
        "Demand": demand,
        "Analyst Hours": analyst_hours_required,
        "Adjuster Hours": adjuster_hours_required,
        "Registration Hours": registration_hours_required
    })

    st.header("Descargar Resultados")
    st.download_button(
        label="Descargar CSV",
        data=results_df.to_csv(index=False),
        file_name="simulacion_capacidad.csv",
        mime="text/csv"
    )

else:
    st.info("Configure los parámetros en la barra lateral y presione 'Ejecutar Simulación'.")
