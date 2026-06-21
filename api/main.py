from fastapi import FastAPI
import sqlite3
import pandas as pd

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