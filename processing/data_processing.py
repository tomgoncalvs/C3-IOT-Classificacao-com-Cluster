import pandas as pd

def preprocess_data(df_compras):
    """
    Pré-processa os dados de compras para calcular métricas de comportamento do usuário.

    Parâmetros:
    - df_compras: DataFrame contendo os dados de compras dos usuários.

    Retorna:
    - df_agrupado: DataFrame contendo métricas agregadas por usuário.
    """
    
    # Convertendo a data de compra para o formato de data
    df_compras['datacompra'] = pd.to_datetime(df_compras['datacompra'])

    # Calculando métricas agregadas para cada usuário
    df_agrupado = df_compras.groupby('usersid').agg({
        'valor': ['mean', 'sum', 'count'],  # Ticket médio, gasto total, número de compras
        'pdvid': 'nunique',  # Número de PDVs diferentes
        'produtoid': 'nunique',  # Número de produtos diferentes comprados
        'categoriaid': 'nunique'  # Número de categorias diferentes compradas
    }).reset_index()

    # Renomeando as colunas para facilitar
    df_agrupado.columns = ['usersid', 'ticket_medio', 'gasto_total', 'num_compras', 'num_pdvs', 'num_produtos', 'num_categorias']

    return df_agrupado
