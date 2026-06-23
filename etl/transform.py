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



def transformar(df_csv, datos_api=None):
    # 1. limpieza actual del CSV
    print("Limpiando datos del CSV...")
    df_limpio = df_csv.copy()
    
    # Asegurarnos de que no haya nulos en la columna clave
    if 'PLAYER' in df_limpio.columns:
        df_limpio = df_limpio.dropna(subset=['PLAYER'])

    # 2. FUSIÓN CON LA API
    if datos_api is not None:
        try:
            print("Iniciando fusión con datos de la API...")
            
            # Lo convertimos a DataFrame
            df_api = pd.DataFrame(datos_api)
            
            if 'first_name' in df_api.columns and 'last_name' in df_api.columns:
                # Concatenamos para crear la misma llave que tiene el CSV
                df_api['PLAYER'] = df_api['first_name'] + " " + df_api['last_name']
                
                # Extraemos alguna columna útil para enriquecer el CSV (ej. el equipo)
                # Si el equipo viene como diccionario, extraemos el nombre
                if 'team' in df_api.columns:
                    df_api['TEAM_API'] = df_api['team'].apply(
                        lambda x: x['full_name'] if isinstance(x, dict) else x
                    )
                else:
                    df_api['TEAM_API'] = "Data API" # Respaldo por si falla
                
                # Nos quedamos solo con las columnas que vamos a cruzar
                df_api_mini = df_api[['PLAYER', 'TEAM_API']].drop_duplicates(subset=['PLAYER'])
                
                # Hacemos un Left Join: mantenemos todo el CSV y le pegamos el TEAM_API donde coincida el nombre
                df_limpio = pd.merge(df_limpio, df_api_mini, on='PLAYER', how='left')
                
                # Llenamos los espacios vacíos de los jugadores que no estaban en la API
                df_limpio['TEAM_API'] = df_limpio['TEAM_API'].fillna('No registrado en API')
                
                print("Fusión CSV + API completada con éxito.")
                
        except Exception as e:
            print(f"Advertencia: No se pudo fusionar la API, continuando solo con CSV. Error: {e}")
    
    return df_limpio