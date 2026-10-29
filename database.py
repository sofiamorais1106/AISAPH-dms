# database.py
import os
import pandas as pd
from io import StringIO

def carregar_dados_tabela():
    caminhos = [
        os.path.join("dados", "Assistente CA CVSE_AISAPH-CV -R.csv"),
        "Assistente CA CVSE_AISAPH-CV -R.csv"
    ]
    for caminho in caminhos:
        if os.path.exists(caminho):
            try:
                with open(caminho, 'rb') as f:
                    content = f.read().decode('latin1', errors='replace')
                df = pd.read_csv(StringIO(content), sep=';', header=None)
                df.columns = [f"col_{i}" for i in range(df.shape[1])]
                return df
            except Exception:
                continue
    return pd.DataFrame()

def carregar_departamentos():
    caminhos = [
        os.path.join("dados", "departamentos.csv"),
        "departamentos.csv"
    ]
    for caminho in caminhos:
        if os.path.exists(caminho):
            try:
                with open(caminho, 'rb') as f:
                    content = f.read().decode('latin1', errors='replace')
                return pd.read_csv(StringIO(content), header=None)
            except Exception:
                continue
    return pd.DataFrame()

def carregar_kpis():
    caminhos = [
        os.path.join("dados", "kpi.csv"),
        "kpi.csv"
    ]
    for caminho in caminhos:
        if os.path.exists(caminho):
            try:
                with open(caminho, 'rb') as f:
                    content = f.read().decode('latin1', errors='replace')
                return pd.read_csv(StringIO(content), sep=';')
            except Exception:
                continue
    return pd.DataFrame()