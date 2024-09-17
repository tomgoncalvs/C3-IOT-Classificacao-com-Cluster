import pandas as pd

def export_analysis_to_excel(df_clusters, df_compras):
    """
    Exporta a análise de clusters e compras para um arquivo Excel.

    Parâmetros:
    - df_clusters: DataFrame contendo dados de clusters.
    - df_compras: DataFrame contendo dados de compras.

    Retorna:
    - Nenhum. Exporta os dados para um arquivo Excel.
    """
    # Calcular o ticket médio de cada cluster
    cluster_summary = df_clusters.groupby('cluster').agg({
        'ticket_medio': 'mean',
        'gasto_total': 'sum',
        'num_compras': 'sum'
    }).reset_index()

    # Analisar melhor data de compra e PDV com melhor taxa de conversão
    df_compras['mes'] = df_compras['datacompra'].dt.month
    best_month = df_compras.groupby('mes')['valor'].sum().idxmax()
    best_pdv = df_compras.groupby('pdvid')['valor'].sum().idxmax()

    # Análise de vendas por categoria e produto
    df_categoria = df_clusters.groupby(['categoriaid', 'cluster']).agg({
        'valor': 'sum',
        'produtoid': 'count'
    }).reset_index()
    df_categoria = df_categoria.rename(columns={'valor': 'Receita Total por Categoria', 'produtoid': 'Quantidade Vendida por Categoria'})

    df_produto = df_clusters.groupby(['produtoid', 'cluster']).agg({
        'valor': 'sum'
    }).reset_index()
    df_produto = df_produto.rename(columns={'valor': 'Receita Total por Produto'})
    df_produto['Quantidade Vendida por Produto'] = df_clusters.groupby('produtoid')['produtoid'].transform('count')

    # Mesclar as análises de categorias e produtos com os dados de clusters
    cluster_analise = pd.merge(cluster_summary, df_categoria, on='cluster', how='left')
    cluster_analise = pd.merge(cluster_analise, df_produto, on='cluster', how='left')

    # Adicionar colunas de melhor mês e PDV
    cluster_analise['Melhor Mês para Compras'] = best_month
    cluster_analise['PDV com Melhor Taxa de Conversão'] = best_pdv

    # Exportar para Excel
    cluster_analise.to_excel('cluster_analysis.xlsx', index=False)
    print("Análise exportada para cluster_analysis.xlsx.")
