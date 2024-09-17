from sklearn.cluster import KMeans
import pandas as pd

def apply_kmeans_clustering(df_agrupado):
    """
    Aplica o algoritmo K-Means para agrupar os usuários em clusters.

    Parâmetros:
    - df_agrupado: DataFrame contendo as informações agregadas dos usuários.

    Retorna:
    - df_agrupado: DataFrame com a coluna de cluster adicionada.
    """
    # Definir o número de clusters como 4 (para clusters 6, 7, 8, 9)
    kmeans = KMeans(n_clusters=4, random_state=42)

    # Ajustar o modelo e prever clusters
    df_agrupado['cluster'] = kmeans.fit_predict(df_agrupado[['ticket_medio', 'gasto_total', 'num_compras', 'num_pdvs']])

    # Mapear os clusters para os valores 6, 7, 8, 9
    df_agrupado['cluster'] = df_agrupado['cluster'].map({0: 6, 1: 7, 2: 8, 3: 9})

    return df_agrupado
