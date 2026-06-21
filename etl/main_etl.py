import logging
from extract import extraer_csv, extraer_api
from transform import transformar  
from load import cargar_a_sqlite           

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def ejecutar_pipeline():
    logging.info("=== Iniciando Pipeline ETL de la NBA ===")
    print("Iniciando Pipeline ETL...")
    
    try:
        # 1. Extracción
        print("1. Extrayendo datos...")
        df_csv = extraer_csv()
        datos_api = extraer_api()
        
        # 2. Transformación
        print("2. Transformando y limpiando datos...")
        
        df_limpio = transformar(df_csv) 
        
        # 3. Carga
        print("3. Cargando datos en SQLite...")
        cargar_a_sqlite(df_limpio)
        
        print("Pipeline finalizado con éxito.")
        logging.info("=== Pipeline ETL finalizado con éxito ===")

    except Exception as e:
        logging.error(f"Error crítico en el pipeline: {e}")
        print(f" Ocurrió un error: {e}")

if __name__ == "__main__":
    ejecutar_pipeline()