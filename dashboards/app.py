import streamlit as st
import pandas as pd
import requests
import os

API_URL = os.environ.get("API_URL", "http://api:8000")

st.title("Dashboard NBA")

# Obtenemos los datos de la API
try:
    stats = requests.get(f"{API_URL}/stats").json()
    jugadores_data = requests.get(f"{API_URL}/players").json()
    lista_jugadores = jugadores_data.get("players", [])
except Exception as e:
    st.error(f"Error conectando a la API: {e}")
    stats = None
    lista_jugadores = []

# --- SEPARAR POR AUDIENCIAS ---
tab1, tab2 = st.tabs(["Vista Ejecutiva (Macro)", "Vista Scouting (Micro)"])

# ---------------------------------------------------------
# AUDIENCIA 1: EJECUTIVOS (Quieren ver resúmenes y tops)
# ---------------------------------------------------------
with tab1:
    st.header("Indicadores Globales de la Liga")
    
    if stats:
        # Tus KPIs globales actuales van aquí
        col1, col2, col3 = st.columns(3)
        col1.metric("Puntos Promedio", stats.get("promedio_puntos", 0))
        col2.metric("Asist. Promedio", stats.get("promedio_asistencias", 0))
        col3.metric("Rebotes Promedio", stats.get("promedio_rebotes", 0))
    
    st.divider()
    
    # EL GRÁFICO OBLIGATORIO
    st.subheader("Top 10 Anotadores")
    if lista_jugadores:
        df_exec = pd.DataFrame(lista_jugadores)
        df_exec["PTS"] = pd.to_numeric(df_exec["PTS"], errors='coerce')
        top_10 = df_exec.nlargest(10, "PTS")
        
        # Gráfico de barras nativo de Streamlit
        st.bar_chart(data=top_10, x="PLAYER", y="PTS")

# ---------------------------------------------------------
# AUDIENCIA 2: ANALISTAS TECNICOS (Quieren buscar al detalle)
# ---------------------------------------------------------
with tab2:
    st.header("Buscador Individual de Jugadores")
    
    # buscador interactivo
    if lista_jugadores:
        df_scout = pd.DataFrame(lista_jugadores)
        
        # Buscador
        jugador_buscado = st.selectbox("Selecciona un jugador:", df_scout["PLAYER"].unique())
        
        if jugador_buscado:
            datos_jugador = df_scout[df_scout["PLAYER"] == jugador_buscado].iloc[0]
            st.write(f"**Puntos:** {datos_jugador['PTS']}")
            st.write(f"**Asistencias:** {datos_jugador['AST']}")
            st.write(f"**Rebotes:** {datos_jugador['REB']}")
            
    st.divider()
    
    st.subheader("Dispersión: Puntos vs Asistencias")
    if lista_jugadores:
        df_scout["PTS"] = pd.to_numeric(df_scout["PTS"], errors='coerce')
        df_scout["AST"] = pd.to_numeric(df_scout["AST"], errors='coerce')
        
        # Gráfico de dispersión (Scatter plot)
        st.scatter_chart(data=df_scout, x="PTS", y="AST")