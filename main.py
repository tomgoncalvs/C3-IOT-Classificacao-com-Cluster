from db.db_connector import load_data_from_oracle, update_user_cluster
from processing.data_processing import preprocess_data
from clustering.clustering import apply_kmeans_clustering
from marketing.marketing_campaign import generate_marketing_campaigns
from model.model_training import train_classification_model, predict_cluster, load_trained_model
from analysis.analysis import export_analysis_to_excel
from interface.interface import generate_campaign_interface
import datetime

def main():
    # Carregar os dados do banco de dados Oracle
    df_compras, df_clusters_info = load_data_from_oracle()

    # Pré-processar os dados para o modelo de clustering
    df_agrupado = preprocess_data(df_compras)

    # Aplicar o modelo de clustering para segmentar os usuários
    df_clusters = apply_kmeans_clustering(df_agrupado)

    # Combine os dados de compras, clusters e informações adicionais dos clusters
    df_combinado = df_compras.merge(df_clusters[['usersid', 'ticket_medio', 'gasto_total', 'num_compras', 'cluster']], on='usersid', how='left')
    df_combinado = df_combinado.merge(df_clusters_info[['clusterid', 'name']], left_on='cluster', right_on='clusterid', how='left')

    # Exportar a análise do cluster para Excel
    export_analysis_to_excel(df_combinado, df_compras)

    # Verificar se já existe um modelo treinado
    model, last_execution_date = load_trained_model()

    # Se o modelo não existir ou a última execução for antiga, treinar um novo modelo
    if model is None or last_execution_date < df_compras['datacompra'].max():
        model = train_classification_model(df_clusters)
    
    # Atualizar a tabela tb_user_cluster com novos dados
    update_user_cluster(df_clusters, model)

    # Interface para geração de campanhas usando o DataFrame combinado
    generate_campaign_interface(model, df_combinado)

if __name__ == "__main__":
    main()
