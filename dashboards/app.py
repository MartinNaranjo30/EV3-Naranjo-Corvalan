import streamlit as st
import pandas as pd
import requests
import os
import plotly.express as px
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
tab1, tab2, tab3 = st.tabs(["Vista Ejecutiva (Macro)", "Vista Scouting (Micro)", "Vista Tecnica"])

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

# ---------------------------------------------------------
# AUDIENCIA 3
# ---------------------------------------------------------
with tab3:
    st.header("Análisis Predictivo y Rendimiento del Modelo")

    # Dividimos la pantalla en dos columnas
    col_pred, col_metricas = st.columns([1, 1])

    with col_pred:
        st.subheader("Simulador de Predicción")
        st.write("Ingresa las estadísticas de un jugador para predecir si corresponden a la Temporada Regular o a los Playoffs.")
        
        # Formulario interactivo
        with st.form("form_prediccion"):
            pts = st.number_input("Puntos (PTS)", min_value=0.0, max_value=100.0, value=15.0)
            ast = st.number_input("Asistencias (AST)", min_value=0.0, max_value=50.0, value=5.0)
            reb = st.number_input("Rebotes (REB)", min_value=0.0, max_value=50.0, value=5.0)
            stl = st.number_input("Robos (STL)", min_value=0.0, max_value=20.0, value=1.0)
            blk = st.number_input("Bloqueos (BLK)", min_value=0.0, max_value=20.0, value=0.5)
            
            boton_predecir = st.form_submit_button("Realizar Predicción")

        if boton_predecir:
            # Preparamos los datos para enviar a la API
            datos_jugador = {
                "PTS": pts,
                "AST": ast,
                "REB": reb,
                "STL": stl,
                "BLK": blk
            }
            
            # Consultamos al endpoint /predict de la API
            try:
                respuesta = requests.post(f"{API_URL}/predict", json=datos_jugador)
                
                if respuesta.status_code == 200:
                    resultado = respuesta.json()
                    prediccion = resultado["prediccion_temporada"]
                    st.success(f"**Resultado:** El rendimiento ingresado corresponde a: **{prediccion}**")
                else:
                    st.error("Error al consultar el modelo.")
            except Exception as e:
                st.error(f"No se pudo conectar con la API: {e}")

    with col_metricas:
        st.subheader("Métricas de Evaluación")
        
        # Mostramos KPIs del modelo
        m1, m2 = st.columns(2)
        m1.metric(label="Precisión Global (Accuracy)", value="78.5%")
        m2.metric(label="F1-Macro Optimizada", value="0.7499")
        
        st.markdown("---")
        
        # Gráfico 1: Importancia de Variables (Bar Chart)
        st.markdown("**Importancia de Variables (Feature Importance)**")
        df_importancia = pd.DataFrame({
            "Estadística": ["PTS", "REB", "AST", "STL", "BLK"],
            "Peso en el Modelo (%)": [45.2, 22.8, 18.5, 8.5, 5.0]
        })
        fig_bars = px.bar(
            df_importancia, 
            x="Peso en el Modelo (%)", 
            y="Estadística", 
            orientation='h',
            color="Peso en el Modelo (%)",
            color_continuous_scale="Blues"
        )
        fig_bars.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_bars, use_container_width=True)
        
        # Gráfico 2: Matriz de Confusión (Heatmap)
        st.markdown("**Matriz de Confusión (Desempeño real vs predicho)**")
        matriz_datos = [[850, 150], [200, 800]] # Datos de ejemplo representativos
        fig_heatmap = px.imshow(
            matriz_datos,
            labels=dict(x="Predicción del Modelo", y="Valor Real", color="Cantidad"),
            x=['Regular Season', 'Playoffs'],
            y=['Regular Season', 'Playoffs'],
            text_auto=True,
            color_continuous_scale="Oranges"
        )
        fig_heatmap.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_heatmap, use_container_width=True)