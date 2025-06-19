Scraper de Vagas com AWS Lambda e CloudFormation

Um sistema de web scraping serverless e automatizado para monitorar vagas de emprego em tecnologia. O projeto utiliza AWS Lambda para execução, EventBridge para agendamento e S3 para armazenamento. Toda a infraestrutura é provisionada via AWS CloudFormation.

✨ Features
Automação Diária: Executa buscas automaticamente uma vez por dia.

Busca Configurável: As queries de busca são facilmente gerenciadas através de um arquivo de texto (urls_to_scan.txt).

Armazenamento Persistente: Salva todos os resultados encontrados em formato JSON em um bucket S3.

Infraestrutura como Código (IaC): Deploy rápido, consistente e replicável com um único arquivo do CloudFormation.

Serverless: Baixo custo e sem necessidade de gerenciar servidores.

🏗️ Arquitetura e Fluxo de Dados
O processo é simples e robusto, orquestrado inteiramente por serviços da AWS.

┌────────────────────────┐      ┌────────────────────┐      ┌─────────────────────────┐
│  Amazon EventBridge    │──────►│    AWS Lambda      │───► │  SerpApi (Google Search)│
│ (Agendador 'Cron')     │      │ (Função Python)    │      └─────────────────────────┘
└────────────────────────┘      └─────────┬──────────┘
                                          │
                                          ▼
                                ┌────────────────────┐
                                │   Amazon S3 Bucket │
                                │ (Armazena .json)   │
                                └────────────────────┘

EventBridge dispara a função Lambda no horário agendado.

Lambda lê as queries do arquivo urls_to_scan.txt.

A função chama a SerpApi para cada query.

Os resultados são processados e as vagas relevantes são salvas em um arquivo JSON no S3.

🛠️ Tech Stack
Cloud: Amazon Web Services (AWS)

Computação: AWS Lambda

Armazenamento: Amazon S3

Agendamento: Amazon EventBridge

IaC: AWS CloudFormation

Linguagem: Python 3.11

API Externa: SerpApi

🚀 Guia de Instalação e Deploy
Para colocar este projeto em produção, siga os passos abaixo.

Pré-requisitos
Conta na AWS com AWS CLI configurado.

Python e pip instalados.

Uma chave de API da SerpApi.

Um bucket S3 para armazenar o código da aplicação (deployment_package.zip).

Passos para o Deploy
Clone este repositório:

git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>

Personalize as buscas:
Edite o arquivo urls_to_scan.txt para incluir suas próprias queries de busca.

Crie o pacote de deploy:
Este comando instala as dependências e cria o arquivo .zip pronto para upload.

# Instala dependências na pasta local
pip install -r requirements.txt -t .

# Cria o arquivo .zip
zip -r deployment_package.zip .

Faça upload do código para o S3:

aws s3 cp deployment_package.zip s3://<SEU_BUCKET_DE_CODIGO>/

Implante a stack com CloudFormation:
Execute o comando abaixo, substituindo os valores dos parâmetros.

aws cloudformation deploy \
  --template-file template.yaml \
  --stack-name "DailyJobScraperStack" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    SerpApiKey="SUA_CHAVE_SECRETA_DA_SERPAPI" \
    DataS3BucketName="seu-bucket-de-dados-de-saida" \
    LambdaCodeS3Bucket="seu-bucket-de-codigo"

Usage
Após o deploy, a função será executada automaticamente no horário definido (padrão: 12:00 UTC). Os resultados aparecerão no seu bucket S3 de dados, organizados em arquivos JSON com a data e hora da execução no nome.

Para um teste imediato, você pode invocar a função Lambda manualmente através do Console da AWS.

🤝 Contribuições
Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir um Pull Request ou relatar um problema (Issue).

Este projeto é distribuído sob a licença MIT.
