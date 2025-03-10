import pandas as pd
import os

def preparar_arquivo(origem, destino):
    # Lê o arquivo original
    dados = pd.read_csv(origem, delimiter=r'\s+', header=None, engine='python')

    # Salva o arquivo em um novo formato com espaços simples como delimitadores
    dados.to_csv(destino, sep=' ', index=False, header=False)

def processar_arquivos(pasta_origem, pasta_destino):
    # Verifica se a pasta de destino existe, caso contrário, cria
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Lista todos os arquivos na pasta de origem
    arquivos = [f for f in os.listdir(pasta_origem) if f.endswith('.csv')]

    for arquivo in arquivos:
        # Define o caminho de origem e destino com o mesmo nome
        origem = os.path.join(pasta_origem, arquivo)
        destino = os.path.join(pasta_destino, arquivo)  # Salva na pasta de destino com o mesmo nome
        
        # Chama a função para processar e salvar o novo arquivo
        preparar_arquivo(origem, destino)
        print(f"Arquivo {arquivo} processado e salvo como: {destino}")

# Defina os caminhos das pastas
pasta_origem = './src/prog2021/'
pasta_destino = './src/prog2021_formatado/'

# Processa todos os arquivos CSV na pasta de origem
processar_arquivos(pasta_origem, pasta_destino)