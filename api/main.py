from fastapi import FastAPI
import sqlite3
import pandas as pd
import joblib
from pydantic import BaseModel
import os

app = FastAPI(title = "API NBA")

def get_db_connection():
  conn = sqlite3.connect("/app/data/nba.db")
  conn.row_factory = sqlite3.Row
  return conn



@app.get("/players")

def get_players():
  conn = get_db_connection()
  cursor = conn.execute("SELECT * FROM nba_clean LIMIT 100")
  rows = [dict(row) for row in cursor.fetchall()]
  conn.close()
  return {"total": len(rows), "players": rows}


@app.get("/stats")

def get_stats():
  conn = get_db_connection()
  df = pd.read_sql("SELECT * FROM nba_clean", conn)
  conn.close()
  return {
    "total_registros": len(df),
    "promedio_puntos": round(df["PTS"].mean(), 2),
    "promedio_asistencias": round(df["AST"].mean(), 2),
    "promedio_rebotes": round(df["REB"].mean(), 2),
  }

class JugadorStats(BaseModel):
    PTS: float
    AST: float
    REB: float
    STL: float
    BLK: float


@app.post("/predict")
def predecir_rendimiento(stats: JugadorStats):
    """
    Recibe las estadísticas de un jugador y predice a qué tipo de temporada
    corresponde su rendimiento usando el modelo de Machine Learning.
    """
    ruta_modelo = "models/modelo_nba.pkl"

    if not os.path.exists(ruta_modelo):
        return {"error": "El modelo no ha sido entrenado o no se encuentra en la ruta."}

    modelo_cargado = joblib.load(ruta_modelo)
    datos_entrada = [[stats.PTS, stats.AST, stats.REB, stats.STL, stats.BLK]]
    prediccion = modelo_cargado.predict(datos_entrada)

    return {
        "mensaje": "Predicción exitosa",
        "prediccion_temporada": prediccion[0]
    }