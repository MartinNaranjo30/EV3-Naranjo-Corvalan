import sqlite3
import logging

def cargar_a_sqlite(df, db_path="/app/data/nba.db"):
  try:
    conn = sqlite3.connect(db_path)
    df.to_sql("nba_clean", conn, if_exists="replace", index=False)
    conn.close()
    logging.info(f"Datos cargados a SQLite: {len(df)} registros")
  except Exception as e:
    logging.error(f"Error al cargar a SQLite: {e}")