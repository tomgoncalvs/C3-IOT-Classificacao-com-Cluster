# Classificação em Clusters com Inteligência Artificial

## Descrição do Projeto

Este projeto classifica usuários com base em seu comportamento de compra utilizando técnicas de Inteligência Artificial. O objetivo é agrupar usuários em clusters e gerar campanhas de marketing personalizadas para cada grupo, melhorando a segmentação e eficácia das estratégias de marketing.

## Estrutura do Projeto

- **data_processing.py**: Processa e organiza os dados das compras dos usuários.
- **clustering.py**: Aplica o algoritmo de K-Means para agrupar os usuários com base em características de compra.
- **model_training.py**: Treina um modelo de Random Forest para prever clusters de novos usuários com base em dados históricos.
- **marketing_campaign.py**: Gera campanhas de marketing personalizadas para cada cluster de usuários, utilizando a API da OpenAI.
- **interface.py**: Interface para o usuário interagir com o sistema, selecionando clusters e avaliando as campanhas geradas.
- **db_connector.py**: Conecta ao banco de dados Oracle para carregar dados de compras e informações de clusters.
- **config/config.py**: Configurações do projeto, incluindo chaves de API e credenciais de banco de dados.

## Banco de Dados Utilizado

O projeto utiliza um banco de dados **Oracle** para armazenar informações de compras, produtos, categorias e clusters de usuários. Para conectar ao banco de dados Oracle, é necessário o uso do **Oracle Instant Client**.

### Instalação do Oracle Instant Client

#### Windows

1. Acesse o site da Oracle e faça o download do [Oracle Instant Client para Windows](https://www.oracle.com/database/technologies/instant-client/downloads.html).
2. Extraia o conteúdo do arquivo ZIP baixado para um diretório de sua escolha (exemplo: `C:\oracle\instantclient_21_3`).
3. Adicione o diretório do Instant Client ao PATH do sistema:
   - Clique com o botão direito em "Este Computador" > "Propriedades".
   - Clique em "Configurações Avançadas do Sistema" > "Variáveis de Ambiente".
   - Na seção "Variáveis de Sistema", encontre a variável `PATH` e clique em "Editar".
   - Adicione o caminho completo do diretório onde o Oracle Instant Client foi extraído (exemplo: `C:\oracle\instantclient_21_3`).

### macOS

1. Acesse o site da Oracle e faça o download do [Oracle Instant Client para macOS](https://www.oracle.com/database/technologies/instant-client/downloads.html).
2. Extraia o conteúdo do arquivo ZIP baixado para um diretório (exemplo: `/Users/seu_usuario/Downloads/instantclient_19_8`).
3. No terminal, configure a variável de ambiente para o Oracle Instant Client:
   ```bash
   export DYLD_LIBRARY_PATH=/Users/seu_usuario/Downloads/instantclient_19_8:$DYLD_LIBRARY_PATH

4. Instale as dependências do projeto, incluindo o `cx_Oracle`, utilizando o comando:
   ```bash
   pip install -r requirements.txt

### Fluxo de Trabalho

1. **Processamento de Dados**: Limpeza e organização dos dados de compras para gerar características dos usuários.
2. **Clustering**: Agrupamento de usuários usando K-Means para identificar padrões de comportamento.
3. **Treinamento do Modelo**: Utilização de Random Forest para prever clusters de novos usuários com base em dados anteriores.
4. **Geração de Campanhas**: Criação de campanhas de marketing direcionadas para cada cluster de usuários.
5. **Interação com o Usuário**: O sistema solicita feedback e permite reclassificação das campanhas com base na avaliação do usuário.
6. **Exportação**: Campanhas aprovadas são exportadas para um arquivo `.txt` para futuras análises.

### Escolha dos Modelos

Optamos pelo **K-Means** para o agrupamento inicial devido à sua eficiência em identificar grupos de dados de forma não supervisionada, ideal para identificar padrões de comportamento de compra sem rótulos prévios. O **Random Forest** foi escolhido pela sua capacidade robusta de lidar com dados complexos e fornecer previsões facilmente interpretáveis.

### Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Scikit-Learn**: Ferramenta para aplicar algoritmos de Machine Learning, como K-Means e Random Forest.
- **OpenAI API**: Utilizada para gerar conteúdo de campanhas de marketing personalizadas.
- **cx_Oracle**: Biblioteca para conectar e interagir com o banco de dados Oracle.
- **Docx**: Biblioteca para exportar documentações e relatórios.

### Instalação e Execução

Instale as dependências com:

pip install -r requirements.txt

Execute com python main.py

### Exportação e Aprendizado Contínuo

O sistema permite que o usuário avalie as campanhas geradas, fornecendo feedback. Se a nota dada pelo usuário for menor que 7, ele pode inserir sugestões para ajustar a campanha e gerar novamente. O sistema aprende continuamente a partir desse feedback e dos novos dados inseridos, garantindo que as futuras campanhas sejam mais relevantes e eficazes.

### Estrutura do Banco de Dados

O projeto utiliza um banco de dados Oracle que armazena informações de compras, produtos e categorias. As tabelas principais incluem:

- **tb_compras**: Registros de compras feitas pelos usuários.
- **tb_produtos**: Detalhes dos produtos comprados.
- **tb_categorias**: Categorias a que os produtos pertencem.
- **tb_user_cluster**: Mapeamento de usuários para clusters após a classificação.

### Contribuição

Este projeto está em desenvolvimento contínuo. Feedbacks e sugestões são bem-vindos para aprimoramentos futuros!

### Licença

Este projeto é disponibilizado sob a Licença MIT.
