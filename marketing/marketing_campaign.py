import openai
from config.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_marketing_campaigns(df_combined):
    """
    Gera campanhas de marketing para cada cluster de usuários.

    Parâmetros:
    - df_combined: DataFrame contendo as informações combinadas de clusters e compras dos usuários.
    """
    # Mapear cluster IDs para classes sociais
    cluster_to_class = {
        6: "clientes com médio-alto poder aquisitivo",
        7: "clientes com poder aquisitivo médio",
        8: "clientes com poder aquisitivo baixo",
        9: "clientes com muito baixo poder aquisitivo"
    }

    for cluster_name in df_combined['name'].unique():
        cluster_data = df_combined[df_combined['name'] == cluster_name]

        # Identificar a classe social do cluster
        cluster_id = cluster_data['cluster'].iloc[0]
        classe_social = cluster_to_class.get(cluster_id, "clientes")

        # Determinar o produto mais vendido e a categoria correspondente
        produto_mais_vendido_id = cluster_data['produtoid'].mode()[0]
        produto_mais_vendido_nome = cluster_data[cluster_data['produtoid'] == produto_mais_vendido_id]['produto_nome'].iloc[0]
        categoria_mais_vendida = cluster_data[cluster_data['produtoid'] == produto_mais_vendido_id]['categoria_nome'].mode()[0]

        # Função para gerar o prompt inicial
        def gerar_prompt(feedback=None):
            prompt = (
                f"Crie uma campanha de marketing para {classe_social}. "
                f"O produto mais vendido neste segmento é '{produto_mais_vendido_nome}', "
                f"que pertence à categoria '{categoria_mais_vendida}'. "
            )
            if feedback:
                prompt += f"Incorpore o seguinte feedback do usuário: {feedback}."
            else:
                prompt += (
                    f"Baseando-se nestas informações, desenvolva uma campanha que seja atraente para {classe_social}, "
                    f"destacando o produto '{produto_mais_vendido_nome}' e sua categoria '{categoria_mais_vendida}' de forma eficaz."
                )
            return prompt

        # Geração da campanha inicial
        prompt = gerar_prompt()
        campaign_text = generate_campaign(prompt)

        # Interação com o usuário para avaliação
        while True:
            print(f"Campanha para Cluster {cluster_name} ({classe_social}):\n{campaign_text}\n")
            rating = input("Avalie a campanha gerada de 0 a 10: ")

            try:
                rating = int(rating)
            except ValueError:
                print("Por favor, insira um número válido entre 0 e 10.")
                continue

            if rating >= 7:
                print("Campanha aprovada.")
                export_campaign_to_txt(cluster_name, classe_social, campaign_text)
                break
            else:
                feedback = input("Por favor, forneça um feedback para melhorar a campanha: ")
                print("Gerando nova campanha com base no feedback...")
                prompt = gerar_prompt(feedback)
                campaign_text = generate_campaign(prompt)

def generate_campaign(prompt):
    """
    Gera uma campanha de marketing com base em um prompt fornecido.

    Parâmetros:
    - prompt: String com o prompt a ser enviado para o modelo de IA.

    Retorna:
    - String com o texto da campanha gerada.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um especialista em marketing."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    return response['choices'][0]['message']['content'].strip()

def export_campaign_to_txt(cluster_name, classe_social, campaign_text):
    """
    Exporta a campanha gerada para um arquivo .txt.

    Parâmetros:
    - cluster_name: Nome do cluster.
    - classe_social: Descrição da classe social do cluster.
    - campaign_text: Texto da campanha a ser exportada.
    """
    file_name = f"campanha_{cluster_name.replace(' ', '_').lower()}.txt"
    with open(file_name, 'w') as file:
        file.write(f"Campanha para Cluster {cluster_name} ({classe_social}):\n\n")
        file.write(campaign_text)
    print(f"Campanha exportada para {file_name}.")
