import requests
import pandas as pd

def main():
    # Configura parâmetros conforme seu código
    frequencia  = 60  # Hz
    T           = 1 / frequencia
    amostras    = int(T * 10**5)
    aux         = 3
    qtd_Dados   = aux * amostras
    url = "http://localhost:5000/classificar"
    
    # [10, 13, 14, 15]
    # Leitura dos dados (pandas)
    L = 15
    dados = pd.read_csv(f"./src/prog2021/L{L}.csv", delimiter="  ", header=None, engine='python').iloc[:qtd_Dados, 1:2]
    dados = pd.DataFrame(dados.values.reshape(-1,1666)) * 10000
    
    # Converter para lista
    dados_json = {"dados": dados.values.tolist()}

    # Enviar requisição para a API
    response = requests.post(url, json=dados_json)
    
    if response.status_code == 200:
        resultado = response.json().get("classe")
        print(f"Classe encontrada: {resultado}")
    else:
        print(f"Erro na requisição: {response.text}")

if __name__ == "__main__":
    main()