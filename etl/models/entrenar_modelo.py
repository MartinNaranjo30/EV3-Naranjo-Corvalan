import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

def entrenar_y_guardar():
    print("1. Cargando datos limpios desde la base de datos SQLite...")
    directorio_actual = os.getcwd()
    db_path = os.path.join(directorio_actual, "data", "nba.db")
    
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        df = pd.read_sql_query("SELECT * FROM nba_clean", conn)
        conn.close()
        print("Base de datos leída.")
    except Exception as e:
        print(f"Error al conectar: {e}")
        return

    # Definición de variables predictoras y objetivo
    features = ['PTS', 'AST', 'REB', 'STL', 'BLK']
    target = 'Season_type'

    df_modelo = df.dropna(subset=features + [target]).copy()
    X = df_modelo[features]
    y = df_modelo[target]

    print("2. Separando datos de entrenamiento y prueba...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("3. Ejecutando Optimización de Hiperparámetros con Validación Cruzada...")
    param_grid = {
        'max_depth': [3, 5, 7, 10, None],
        'min_samples_split': [2, 5, 10],
        'criterion': ['gini', 'entropy']
    }

    # Se inicia el modelo base
    modelo_base = DecisionTreeClassifier(random_state=42)

    # Configuramos la validación cruzada (cv=5)
    grid_search = GridSearchCV(estimator=modelo_base, param_grid=param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # Extraemos el modelo ganador
    mejor_modelo = grid_search.best_estimator_
    print(f"Mejores hiperparámetros encontrados: {grid_search.best_params_}")

    print("4. Evaluando métricas de negocio complejas...")
    y_pred = mejor_modelo.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Precisión Global (Accuracy): {accuracy:.4f}")
    
    print("\n Reporte de Clasificación (Precision, Recall, F1-Score):")
    print(classification_report(y_test, y_pred))
    
    print("\n Matriz de Confusión:")
    print(confusion_matrix(y_test, y_pred))

    print("5. Serializando y guardando el modelo optimizado...")
    os.makedirs('etl/models', exist_ok=True)
    ruta_guardado = 'etl/models/modelo_nba.pkl'
    joblib.dump(mejor_modelo, ruta_guardado)
    
    print(f"El modelo predictivo fue guardado como {ruta_guardado}")

if __name__ == '__main__':
    entrenar_y_guardar()

    