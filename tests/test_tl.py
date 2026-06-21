import pandas as pd
from etl.transform import validar_esquema, limpiar_nulos, transformar

def test_limpiar_nulos():

  df = pd.DataFrame({"PTS": [10, None, 20], "AST": [1,2,3], "REB": [1,2,3]})
  resultado = limpiar_nulos(df)
  assert len(resultado) == 2

def test_validar_esquema():

  df = pd.DataFrame({"PTS": ["10", "20"], "AST": [1,2], "REB":[1,2], "STL":[1,1], "BLK":[1,1], "TOV":[1,1], "EFF":[1,1]})
  resultado = validar_esquema(df)
  assert resultado["PTS"].dtype != object

def test_transformar_no_falla():

  df = pd.DataFrame({"PTS": [10, "malo"], "AST":[1,2], "REB":[1,2], "STL":[1,1], "BLK":[1,1], "TOV":[1,1], "EFF":[1,1]})
  resultado = transformar(df)
  assert resultado is not None