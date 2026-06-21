import pandas as pd
import requests
import logging

logging.basicConfig(
  filename="etl_pipeline.log",
  level=logging.INFO,
  format="%(asctime)s - %(levelname)s - %(message)s"
)



def extraer_csv(path="/app/data/nba_10000_dirty.csv"):
  try:
    df = pd.read_csv(path)
    logging.info(f"CSV extraído correctamente: {len(df)} filas")
    return df
  except Exception as e:
    logging.error(f"Error al leer el CSV: {e}")
    return pd.DataFrame()



def extraer_api():
  try:
    resp = requests.get("https://www.balldontlie.io/api/v1/players", timeout=5)
    resp.raise_for_status()
    data = resp.json()

    logging.info("Datos de API extraídos correctamente")
    return data
  except Exception as e:
    logging.error(f"Error al conectar con la API: {e}")
    return {}