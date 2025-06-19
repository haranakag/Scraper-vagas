Scraper de Vagas de TI com AWS Lambda
Este projeto implementa um scraper serverless para coletar vagas de emprego de tecnologia a partir de buscas no Google. A solução é executada em um cronograma diário usando AWS Lambda, e os resultados são armazenados em um bucket S3. A infraestrutura é totalmente gerenciada como código usando um template do AWS CloudFormation.

Sumário
Visão Geral
Arquitetura da Solução
Estrutura do Repositório
Pré-requisitos
Configuração e Deploy
Execução e Verificação
Variáveis de Ambiente
Como Contribuir
Licença
1. Visão Geral
O objetivo deste projeto é automatizar a busca por vagas de emprego específicas. Em vez de realizar buscas manuais diariamente, um processo automatizado é executado na nuvem.

Automação: Uma regra do Amazon EventBridge dispara a função uma vez por dia.
Coleta de Dados: Uma função Python no AWS Lambda lê uma lista de queries de busca, chama a SerpApi para obter os resultados do Google e processa as informações.
Armazenamento: Os dados das vagas encontradas são agregados e salvos como um único arquivo JSON em um bucket do Amazon S3.
Infraestrutura como Código (IaC): Todos os recursos da AWS (Lambda, Role, EventBridge) são provisionados através de um template do AWS CloudFormation, garantindo um deploy consistente e replicável.
2. Arquitetura da Solução
O fluxo de trabalho da aplicação é o seguinte:

Agendador (Amazon EventBridge): Uma regra do tipo "cron" é acionada diariamente.
Gatilho: A regra do EventBridge invoca a função AWS Lambda.
Execução (AWS Lambda): a. A função Python é iniciada. b. Ela lê as queries de busca do arquivo urls_to_scan.txt. c. Para cada query, ela faz uma requisição para a SerpApi. d. A API retorna os resultados da busca do Google em formato JSON. e. O código processa os resultados, procurando por palavras-chave relevantes nos títulos e descrições.
Armazenamento (Amazon S3): Todas as vagas encontradas são compiladas em uma lista e salvas como um arquivo JSON com timestamp em um bucket S3 designado.
3. Estrutura do Repositório
.
├── lambda_function.py      # O código principal da função Lambda.
├── urls_to_scan.txt        # Arquivo de texto com as queries de busca (uma por linha).
├── requirements.txt        # Dependências Python do projeto.
├── template.yaml           # Template do AWS CloudFormation para deploy da infraestrutura.
└── README.md               # Esta documentação.
4. Pré-requisitos
Antes de começar, certifique-se de que você possui:

Uma conta na AWS.
AWS CLI instalado e configurado com suas credenciais.
Python 3.9 ou superior.
Uma conta na SerpApi e sua chave de API secreta.
Dois buckets S3 criados na sua conta AWS:
Um para armazenar o código da Lambda (o pacote .zip).
Outro para armazenar os dados de saída (os arquivos .json).
5. Configuração e Deploy
Siga os passos abaixo para configurar e implantar a solução.

Passo 1: Clonar o Repositório
Bash

git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
Passo 2: Configurar as Queries de Busca
Edite o arquivo urls_to_scan.txt e adicione as queries de busca do Google que você deseja monitorar, uma por linha.

Passo 3: Empacotar a Função Lambda
Para que a AWS Lambda possa executar o código, você precisa empacotá-lo junto com suas dependências.

Bash

# Instalar as dependências na pasta atual
pip install -r requirements.txt -t .

# Criar o arquivo zip com o código, o arquivo de urls e as dependências
zip -r deployment_package.zip .
Passo 4: Fazer Upload do Pacote de Código
Faça o upload do arquivo deployment_package.zip para o seu bucket S3 de código.

Bash

aws s3 cp deployment_package.zip s3://<SEU_BUCKET_DE_CODIGO>/
Passo 5: Fazer o Deploy com CloudFormation
Use a AWS CLI para implantar a stack definida no template.yaml. Substitua os valores dos parâmetros pelos seus.

Bash

aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name daily-job-scraper \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    SerpApiKey="<SUA_CHAVE_SECRETA_DA_SERPAPI>" \
    DataS3BucketName="<SEU_BUCKET_DE_DADOS>" \
    LambdaCodeS3Bucket="<SEU_BUCKET_DE_CODIGO>" \
    LambdaCodeS3Key="deployment_package.zip"
6. Execução e Verificação
Execução Manual (para Testes)
Navegue até o console do AWS Lambda.
Encontre a função criada (ex: daily-job-scraper-AshbyScraperFunction).
Vá para a aba "Test" e crie um evento de teste com qualquer conteúdo JSON (ex: {}).
Clique em "Test" para executar a função imediatamente.
Execução Agendada
A função será executada automaticamente uma vez por dia, conforme definido no parâmetro ScheduleExpression do CloudFormation (padrão: 12:00 UTC).

Verificação dos Resultados
Logs: Verifique os logs da execução no Amazon CloudWatch para depurar ou confirmar que a função rodou sem erros.
Arquivos de Saída: Navegue até o seu bucket S3 de dados. Após uma execução bem-sucedida, você encontrará um novo arquivo .json com os resultados.
7. Variáveis de Ambiente
A função Lambda utiliza as seguintes variáveis de ambiente, que são configuradas automaticamente pelo CloudFormation durante o deploy:

S3_BUCKET_NAME: O nome do bucket S3 de destino para os arquivos JSON.
SERPAPI_API_KEY: Sua chave de API secreta da SerpApi.
8. Como Contribuir
Contribuições são bem-vindas! Por favor, siga o fluxo padrão de desenvolvimento:

Faça um Fork do projeto.
Crie uma nova branch (git checkout -b feature/nova-feature).
Faça o commit das suas alterações (git commit -am 'Adiciona nova feature').
Faça o push para a branch (git push origin feature/nova-feature).
Abra um Pull Request.
9. Licença
Este projeto é licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.
