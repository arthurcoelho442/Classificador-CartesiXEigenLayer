from rede.classificador3 import getClasse
import pandas as pd

def main():
    # Configura parâmetros conforme seu código
    frequencia  = 60  # Hz
    T           = 1 / frequencia
    amostras    = int(T * 10**5)
    aux         = 3
    qtd_Dados   = aux * amostras

    # Leitura dos dados (pandas)
    dados = pd.read_csv("./src/prog2021/L13.csv", delimiter="  ", header=None, engine='python').iloc[:qtd_Dados, 1:2]
    dados = pd.DataFrame(dados.values.reshape(-1,1666))

    # Obter a classificação
    resultado = getClasse(dados)
    print(f"Classe encontrada: {resultado}")

if __name__ == "__main__":
    main()