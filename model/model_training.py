from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import os
import datetime

MODEL_PATH = "cluster_model.pkl"
LAST_EXECUTION_FILE = "last_execution.txt"

def train_classification_model(df_clusters):
    """
    Treina um modelo de classificação RandomForest para prever clusters de usuários.

    Parâmetros:
    - df_clusters: DataFrame contendo as informações de clusters dos usuários.

    Retorna:
    - model: Modelo de classificação treinado.
    """
    # Verificar o conteúdo de df_clusters antes do filtro
    print("Dados antes do filtro:")
    print(df_clusters.head())

    # Filtrar apenas os clusters válidos (6, 7, 8, 9)
    df_clusters = df_clusters[df_clusters['cluster'].isin([6, 7, 8, 9])]

    # Verificar o conteúdo de df_clusters após o filtro
    print("Dados após o filtro:")
    print(df_clusters.head())

    # Verificar se o DataFrame está vazio após o filtro
    if df_clusters.empty:
        raise ValueError("Nenhum dado disponível para treinar o modelo após filtrar os clusters válidos. Verifique os dados de entrada.")

    # Preparar os dados para o treinamento
    X = df_clusters[['ticket_medio', 'gasto_total', 'num_compras', 'num_pdvs', 'num_produtos', 'num_categorias']]
    y = df_clusters['cluster']

    # Treinar o modelo RandomForest
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    # Salvar o modelo treinado
    joblib.dump(model, MODEL_PATH)
    with open(LAST_EXECUTION_FILE, 'w') as f:
        f.write(str(datetime.datetime.now()))

    print("Modelo de classificação treinado e salvo com sucesso.")
    return model

def load_trained_model():
    """
    Carrega o modelo de classificação previamente treinado e a data da última execução.

    Retorna:
    - model: Modelo de classificação treinado.
    - last_execution_date: Data da última execução do treinamento do modelo.
    """
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        with open(LAST_EXECUTION_FILE, 'r') as f:
            last_execution_date = datetime.datetime.strptime(f.read().strip(), '%Y-%m-%d %H:%M:%S.%f')
        return model, last_execution_date
    else:
        print("Modelo treinado não encontrado. Por favor, treine o modelo primeiro.")
        return None, None

def predict_cluster(model, new_purchase):
    """
    Prediz o cluster de um novo usuário com base em suas características de compra.

    Parâmetros:
    - model: Modelo de classificação treinado.
    - new_purchase: Lista contendo as características da nova compra (ticket médio, gasto total, número de compras, número de PDVs, número de produtos, número de categorias).

    Retorna:
    - cluster_prediction: ID do cluster previsto.
    """
    # Verificar se new_purchase contém todas as 6 colunas esperadas
    if len(new_purchase) != 6:
        raise ValueError("Os dados da nova compra devem conter exatamente 6 elementos: ['ticket_medio', 'gasto_total', 'num_compras', 'num_pdvs', 'num_produtos', 'num_categorias']")

    # Prever o cluster para uma nova compra usando um DataFrame para manter os nomes das colunas
    new_purchase_df = pd.DataFrame([new_purchase], columns=['ticket_medio', 'gasto_total', 'num_compras', 'num_pdvs', 'num_produtos', 'num_categorias'])
    cluster_prediction = model.predict(new_purchase_df)
    return cluster_prediction[0]
