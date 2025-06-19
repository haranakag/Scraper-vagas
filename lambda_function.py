import json
import os
import boto3
import requests
from datetime import datetime

# --- Variáveis de Configuração ---
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
SERPAPI_API_KEY = os.environ.get('SERPAPI_API_KEY')

# --- Constantes do Scraper ---
# ### NOVO ###: Nome do arquivo de texto que será incluído no pacote
URL_FILE = 'urls_to_scan.txt' 
# Palavras-chave para procurar nos resultados da busca.
KEYWORDS_TO_FIND = [
    "cloud engineer",
    "security engineer",
    "devsecops",
    "cloud security engineer",
    "site reliability engineer",
    "data scientist"
]

def search_google(query, api_key, start_index=0):
    """Função para fazer a chamada à API da SerpApi."""
    params = {
        "api_key": api_key,
        "engine": "google",
        "q": query,
        "start": start_index,
        "num": 100
    }
    response = requests.get("https://serpapi.com/search.json", params=params)
    response.raise_for_status()
    return response.json()

def lambda_handler(event, context):
    """Ponto de entrada da função Lambda."""
    if not S3_BUCKET_NAME or not SERPAPI_API_KEY:
        return {'statusCode': 500, 'body': json.dumps('Erro: Variáveis de ambiente não configuradas.')}

    s3_client = boto3.client('s3')
    all_findings = []
    processed_links = set()
    max_pages = 2

    try:
        # ### NOVO ###: Abrir e ler o arquivo de texto com as URLs
        # O arquivo está na raiz do ambiente de execução do Lambda, junto com o script.
        with open(URL_FILE, 'r', encoding='utf-8') as f:
            # ### NOVO ###: Loop principal que itera sobre cada linha (query) do arquivo
            for query in f:
                query = query.strip()  # Remove espaços em branco e quebras de linha
                if not query:
                    continue  # Pula linhas em branco

                print(f"--- Processando a query: '{query}' ---")

                # Loop de paginação para a query atual
                for page_num in range(max_pages):
                    print(f"Buscando página {page_num + 1} para a query atual...")
                    start_index = page_num * 100
                    search_results = search_google(query, SERPAPI_API_KEY, start_index)
                    
                    organic_results = search_results.get("organic_results", [])
                    if not organic_results:
                        break

                    for result in organic_results:
                        title = result.get("title", "").lower()
                        snippet = result.get("snippet", "").lower()
                        link = result.get("link", "")

                        if not link or link in processed_links:
                            continue

                        text_to_search = f"{title} {snippet}"
                        for keyword in KEYWORDS_TO_FIND:
                            if keyword.lower() in text_to_search:
                                print(f"  > Palavra-chave encontrada: '{keyword}' no link: {link}")
                                finding = {
                                    "source_query": query,
                                    "found_keyword": keyword,
                                    "job_title": result.get("title"),
                                    "link": link,
                                    "snippet": result.get("snippet"),
                                    "retrieved_at": datetime.utcnow().isoformat()
                                }
                                all_findings.append(finding)
                                processed_links.add(link)
                                break
        
        if not all_findings:
            message = "Nenhum resultado encontrado com as palavras-chave para as queries fornecidas."
            print(message)
            return {'statusCode': 200, 'body': json.dumps(message)}

        timestamp = datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"multi_query_findings_{timestamp}.json"
        json_output = json.dumps(all_findings, indent=4)
        
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_name,
            Body=json_output,
            ContentType='application/json'
        )

        success_message = f"Sucesso! {len(all_findings)} vagas encontradas e salvas em s3://{S3_BUCKET_NAME}/{file_name}"
        print(success_message)
        
        return {'statusCode': 200, 'body': json.dumps(success_message)}

    except FileNotFoundError:
        print(f"Erro: O arquivo de URLs '{URL_FILE}' não foi encontrado no pacote de deploy.")
        return {'statusCode': 500, 'body': json.dumps(f"Erro de configuração: Arquivo '{URL_FILE}' não encontrado.")}
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return {'statusCode': 500, 'body': json.dumps(f"Erro interno: {e}")}