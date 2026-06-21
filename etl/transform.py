import pandas as pd
import logging

ESQUEMA_ESPERADO = {
  "PTS": float, "AST": float, "REB": float,
  "STL": float, "BLK": float, "TOV": float, "EFF": float
}


def validar_esquema(df):
  errores = []
  for columna, tipo_esperado in ESQUEMA_ESPERADO.items():
    if columna not in df.columns:
      errores.append(f"Falta columna requerida: {columna}")
      continue
    try:
      df[columna] = pd.to_numeric(df[columna], errors="coerce")
    except Exception as e:
      errores.append(f"Error de tipo en columna {columna}: {e}")

  if errores:
    for e in errores:
      logging.warning(e)
  return df



def limpiar_nulos(df):
  filas_antes = len(df)
  df_limpio = df.dropna(subset=["PTS", "AST", "REB"])
  filas_despues = len(df_limpio)
  if filas_antes != filas_despues:
    logging.info(f"Se eliminaron {filas_antes - filas_despues} filas con nulos")
  return df_limpio


def transformar(df):
  df = validar_esquema(df)
  df = limpiar_nulos(df)
  logging.info(f"Transformación completa: {len(df)} filas finales")
  return df