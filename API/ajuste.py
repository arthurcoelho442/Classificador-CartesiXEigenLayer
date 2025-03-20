from numpy import rint
import requests
import pandas as pd
import os

def main():
    # Configura parâmetros conforme seu código
    frequencia  = 60  # Hz
    T           = 1 / frequencia
    amostras    = int(T * 10**5)
    aux         = 3
    qtd_Dados   = aux * amostras
    url = "http://localhost:5000/classificar"
    
    # Lista de valores de L
    valores_L = [10, 13, 14, 15]
    
    for L in valores_L:
        caminho_arquivo = f"./src/prog2021/L{L}.csv"
        if not os.path.exists(caminho_arquivo):
            print(f"Arquivo {caminho_arquivo} não encontrado, pulando...")
            continue
        
        # Leitura dos dados (pandas)
        dados_completos = pd.read_csv(caminho_arquivo, delim_whitespace=True, header=None, engine='python')
        
        for i in range(0, len(dados_completos), qtd_Dados):
            try:
                dados = dados_completos.iloc[i:i+qtd_Dados, :]  # Pegando as colunas 1 e 2
                if dados.empty:
                    break
                
                dados_form = dados.iloc[:, 0] * 10000
                dados_form = dados_form.astype(int)
                
                # Converter para lista
                dados_json = {"dados": dados.values.reshape(-1,1666).tolist()}

                # Enviar requisição para a API
                response = requests.post(url, json=dados_json)
                
                if response.status_code == 200:
                    resultado = response.json().get("classe")
                    print(f"Classe encontrada para L={L}, bloco {i//qtd_Dados}: {resultado}")
                    
                    # Se o resultado for igual a L, salvar na nova pasta
                    if resultado == L:
                        pasta_ajust = "./src/prog2021-AJUST"
                        os.makedirs(pasta_ajust, exist_ok=True)
                        caminho_arquivo_ajust = os.path.join(pasta_ajust, f"L{L}.csv")
                        
                        # Salvar os dados no final do arquivo (sem sobrescrever)
                        dados.to_csv(caminho_arquivo_ajust, mode='a', index=False, header=False)
                        
                        print(f"Dados adicionados em {caminho_arquivo_ajust}")
                else:
                    print(f"Erro na requisição para L={L}, bloco {i//qtd_Dados}: {response.text}")
            except Exception as e:
                print(f'str({e})')

if __name__ == "__main__":
    main()