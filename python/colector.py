import sys
from rede.classificador import getClasse
import pandas as pd

def main():
    # Configura parâmetros conforme seu código
    frequencia  = 60  # Hz
    T           = 1 / frequencia
    amostras    = int(T * 10**5)
    aux         = 5
    qtd_Dados   = aux * amostras

    # 10, 13, 14, 15
    # Leitura dos dados
    dados = pd.read_csv("./src/prog2021/L15.csv", delimiter="  ", header=None, engine='python').iloc[:qtd_Dados, 0:1]
    dados  = pd.DataFrame(dados.values.reshape(-1,1666))

    # Obter a classificação
    resultado = getClasse(dados)
    print(f"{resultado}")

if __name__ == "__main__":
    main()