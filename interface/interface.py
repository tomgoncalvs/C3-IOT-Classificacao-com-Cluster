from marketing.marketing_campaign import generate_marketing_campaigns

def generate_campaign_interface(model, df_clusters):
    """
    Interface para gerar campanhas de marketing baseadas nos clusters de clientes.

    Parâmetros:
    - model: Modelo de aprendizado de máquina treinado para prever clusters.
    - df_clusters: DataFrame contendo dados de clusters, incluindo nomes e informações agregadas.

    Retorna:
    - Gera campanhas de marketing sugeridas para o cluster selecionado.
    """
    
    # Exibir opções de clusters usando nomes
    print("Escolha um cluster para gerar campanhas de marketing:")
    cluster_names = df_clusters['name'].unique()
    valid_options = {str(i): name for i, name in enumerate(cluster_names, 1)}

    for option, name in valid_options.items():
        print(f"{option}: Cluster {name}")

    selected_option = input("Digite o número correspondente ao cluster desejado: ")

    # Validar a entrada do usuário
    while selected_option not in valid_options:
        print("Opção inválida. Por favor, selecione um número válido.")
        selected_option = input("Digite o número correspondente ao cluster desejado: ")

    # Filtrar os dados para o cluster selecionado
    selected_cluster_name = valid_options[selected_option]
    df_cluster_filtered = df_clusters[df_clusters['name'] == selected_cluster_name]

    # Gerar campanhas de marketing para o cluster selecionado
    generate_marketing_campaigns(df_cluster_filtered)

    print("Campanhas de marketing geradas com sucesso.")
