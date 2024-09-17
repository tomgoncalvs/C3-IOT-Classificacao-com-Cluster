import cx_Oracle
import pandas as pd
from config.config import ORACLE_HOST, ORACLE_PORT, ORACLE_SERVICE_NAME, ORACLE_USER, ORACLE_PASSWORD
from model.model_training import predict_cluster

# Importação do Oracle Instant Client para MacOS
cx_Oracle.init_oracle_client(lib_dir="/Users/ewertongoncalves/Downloads/instantclient_23_3")

def load_data_from_oracle():
    # Estabelecer conexão com o banco de dados Oracle
    dsn = cx_Oracle.makedsn(ORACLE_HOST, ORACLE_PORT, service_name=ORACLE_SERVICE_NAME)
    connection = cx_Oracle.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=dsn)
    
    # Criar um cursor para executar comandos SQL
    cursor = connection.cursor()

    # Executar query para carregar dados de compras com categorias e produtos
    query_compras = """
    SELECT c.usersid, c.pdvid, c.valor, c.datacompra, p.produtoid, p.nome AS produto_nome, 
           p.categoriaid, cat.nome AS categoria_nome, cat.descricao AS categoria_descricao
    FROM tb_compras c
    JOIN tb_produtos p ON c.produtoid = p.produtoid
    JOIN tb_categorias cat ON p.categoriaid = cat.categoriaid
    """
    cursor.execute(query_compras)
    compras_data = cursor.fetchall()

    # Converter os dados de compras em um DataFrame do Pandas
    df_compras = pd.DataFrame(compras_data, columns=['usersid', 'pdvid', 'valor', 'datacompra', 
                                                     'produtoid', 'produto_nome', 'categoriaid', 
                                                     'categoria_nome', 'categoria_descricao'])

    # Executar query para carregar dados de clusters
    query_clusters = """
    SELECT clusterid, name 
    FROM tb_cluster
    """
    cursor.execute(query_clusters)
    clusters_data = cursor.fetchall()

    # Converter os dados de clusters em um DataFrame do Pandas
    df_clusters = pd.DataFrame(clusters_data, columns=['clusterid', 'name'])

    # Fechar a conexão com o banco de dados
    cursor.close()
    connection.close()

    return df_compras, df_clusters

def update_user_cluster(df_clusters, model):
    # Estabelecer conexão com o banco de dados Oracle
    dsn = cx_Oracle.makedsn(ORACLE_HOST, ORACLE_PORT, service_name=ORACLE_SERVICE_NAME)
    connection = cx_Oracle.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=dsn)
    cursor = connection.cursor()

    # Obter o valor máximo atual de userclusterid
    cursor.execute("SELECT COALESCE(MAX(userclusterid), 0) FROM tb_user_cluster")
    max_id = cursor.fetchone()[0]

    # Obter todos os cluster IDs válidos
    valid_cluster_ids = [6, 7, 8, 9]

    for index, row in df_clusters.iterrows():
        # Prever o cluster do usuário com todos os 6 elementos necessários
        cluster_id = predict_cluster(model, [
            row['ticket_medio'], 
            row['gasto_total'], 
            row['num_compras'], 
            row['num_pdvs'], 
            row['num_produtos'], 
            row['num_categorias']
        ])
        
        # Reclassificar se o cluster_id não for válido
        if cluster_id not in valid_cluster_ids:
            print(f"Cluster ID {cluster_id} não é válido. Reclassificando usuário {row['usersid']} para o cluster mais próximo.")
            
            # Criar DataFrame com os nomes de colunas corretos para o modelo
            input_data = pd.DataFrame([[
                row['ticket_medio'], 
                row['gasto_total'], 
                row['num_compras'], 
                row['num_pdvs'], 
                row['num_produtos'], 
                row['num_categorias']
            ]], columns=['ticket_medio', 'gasto_total', 'num_compras', 'num_pdvs', 'num_produtos', 'num_categorias'])

            # Prever o cluster mais provável usando probabilidades
            cluster_id = valid_cluster_ids[model.predict_proba(input_data).argmax()]

        # Incrementar o max_id para garantir um novo ID único
        max_id += 1

        # Atualizar a tabela tb_user_cluster com a classificação
        query_update = f"INSERT INTO tb_user_cluster (userclusterid, clusterid, userid) VALUES ({max_id}, {cluster_id}, {row['usersid']})"
        cursor.execute(query_update)

    # Commit das mudanças e fechamento da conexão
    connection.commit()
    cursor.close()
    connection.close()
    print("Tabela tb_user_cluster atualizada com sucesso.")

    # Estabelecer conexão com o banco de dados Oracle
    dsn = cx_Oracle.makedsn(ORACLE_HOST, ORACLE_PORT, service_name=ORACLE_SERVICE_NAME)
    connection = cx_Oracle.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=dsn)
    cursor = connection.cursor()

    # Obter o valor máximo atual de userclusterid
    cursor.execute("SELECT COALESCE(MAX(userclusterid), 0) FROM tb_user_cluster")
    max_id = cursor.fetchone()[0]

    # Obter todos os cluster IDs válidos
    cursor.execute("SELECT clusterid FROM tb_cluster")
    valid_cluster_ids = [row[0] for row in cursor.fetchall()]

    for index, row in df_clusters.iterrows():
        # Prever o cluster do usuário com todos os 6 elementos necessários
        cluster_id = predict_cluster(model, [
            row['ticket_medio'], 
            row['gasto_total'], 
            row['num_compras'], 
            row['num_pdvs'], 
            row['num_produtos'], 
            row['num_categorias']
        ])
        
        # Corrigir a previsão para garantir que está dentro dos clusters válidos
        if cluster_id not in valid_cluster_ids:
            print(f"Cluster ID {cluster_id} não é válido. Reclassificando usuário {row['usersid']} para o cluster mais próximo.")
            
            # Criar DataFrame com os nomes de colunas corretos para o modelo
            input_data = pd.DataFrame([[
                row['ticket_medio'], 
                row['gasto_total'], 
                row['num_compras'], 
                row['num_pdvs'], 
                row['num_produtos'], 
                row['num_categorias']
            ]], columns=['ticket_medio', 'gasto_total', 'num_compras', 'num_pdvs', 'num_produtos', 'num_categorias'])

            # Prever o cluster mais provável usando probabilidades
            cluster_id = valid_cluster_ids[model.predict_proba(input_data).argmax()]

        # Incrementar o max_id para garantir um novo ID único
        max_id += 1

        # Atualizar a tabela tb_user_cluster com a classificação
        query_update = f"INSERT INTO tb_user_cluster (userclusterid, clusterid, userid) VALUES ({max_id}, {cluster_id}, {row['usersid']})"
        cursor.execute(query_update)

    # Commit das mudanças e fechamento da conexão
    connection.commit()
    cursor.close()
    connection.close()
    print("Tabela tb_user_cluster atualizada com sucesso.")
