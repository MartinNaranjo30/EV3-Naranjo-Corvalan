import pandas as pd
import pytest

# Importamos la función que queremos probar
from etl.transform import transformar

def test_transformar_fusion_csv_api():
    """
    Test unitario para validar que la función 'transformar' 
    realiza el Left Join correctamente entre el CSV y la API.
    """
    # 1. Preparamos datos simulados simulando el CSV
    df_csv_dummy = pd.DataFrame({
        "PLAYER": ["LeBron James", "Jugador Desconocido"],
        "PTS": [25.0, 10.0]
    })

    # 2. Preparamos datos simulados simulando la respuesta de la API
    datos_api_dummy = [
        {"first_name": "LeBron", "last_name": "James", "team": {"full_name": "Los Angeles Lakers"}}
    ]

    # 3. Ejecutamos nuestra función real con los datos falsos
    df_resultado = transformar(df_csv_dummy, datos_api_dummy)

    # 4. Evaluamos (Asserts) que el comportamiento sea el correcto
    assert not df_resultado.empty, "El DataFrame no debería estar vacío."
    assert "TEAM_API" in df_resultado.columns, "La columna TEAM_API no se creó tras la fusión."
    
    # Validamos que LeBron James recibió el equipo de la API
    equipo_lebron = df_resultado.loc[df_resultado["PLAYER"] == "LeBron James", "TEAM_API"].iloc[0]
    assert equipo_lebron == "Los Angeles Lakers", f"Se esperaba 'Los Angeles Lakers', pero se obtuvo {equipo_lebron}"

    # Validamos que el jugador sin datos en la API reciba el valor por defecto
    equipo_desconocido = df_resultado.loc[df_resultado["PLAYER"] == "Jugador Desconocido", "TEAM_API"].iloc[0]
    assert equipo_desconocido == "No registrado en API", "El manejo de valores nulos post-join falló."