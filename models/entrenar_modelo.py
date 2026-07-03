import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def entrenar_y_guardar():
    print("1. Cargando datos limpios desde la base de datos SQLite...")
    try:
        db_path = os.path.join(BASE_DIR, "data", "nba.db")
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM nba_clean", conn)
        conn.close()
    except Exception as e:
        print(f"Error al conectar con BD: {e}")
        return

    features = ['PTS', 'AST', 'REB', 'STL', 'BLK']
    target = 'Season_type'  # minúscula, así viene en el CSV real

    df_modelo = df.dropna(subset=features + [target]).copy()
    X = df_modelo[features]
    y = df_modelo[target]

    print("2. Separando datos y entrenando el Árbol de Decisión...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = DecisionTreeClassifier(max_depth=5, random_state=42)
    modelo.fit(X_train, y_train)

    print("3. Serializando y guardando el modelo...")
    ruta_guardado = os.path.join(os.path.dirname(__file__), "modelo_nba.pkl")
    joblib.dump(modelo, ruta_guardado)

    print(f"¡Éxito! Modelo guardado como {ruta_guardado}")

if __name__ == '__main__':
    entrenar_y_guardar()