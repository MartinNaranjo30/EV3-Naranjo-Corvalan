import streamlit as st
import requests
import pandas as pd
import os

st.set_page_config(page_title="NBA Dashboard", layout="wide")

API_URL = os.environ.get("API_URL", "http://api:8000")

vista = st.sidebar.selectbox("Selecciona vista", ["Gerencia (KPIs)", "Operaciones (Detalle)"])

if vista == "Gerencia (KPIs)":

  st.title("Vista Ejecutiva — KPIs Generales")
  stats = requests.get(f"{API_URL}/stats").json()
  col1, col2, col3 = st.columns(3)
  col1.metric("Promedio Puntos", stats["promedio_puntos"])
  col2.metric("Promedio Asistencias", stats["promedio_asistencias"])
  col3.metric("Promedio Rebotes", stats["promedio_rebotes"])



else:

  st.title("Vista Operativa — Detalle de Jugadores")
  data = requests.get(f"{API_URL}/players").json()
  df = pd.DataFrame(data["players"])
  equipo_filtro = st.text_input("Filtrar por jugador (nombre contiene):")
  if equipo_filtro:
    df = df[df.apply(lambda row: equipo_filtro.lower() in str(row).lower(), axis=1)]
  st.dataframe(df)