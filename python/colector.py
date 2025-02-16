from rede.classificador import getClasse
import numpy as np

def main():
    # Configura parâmetros conforme seu código
    frequencia  = 60  # Hz
    T           = 1 / frequencia
    amostras    = int(T * 10**5)
    aux         = 5
    qtd_Dados   = aux * amostras

    # Leitura dos dados
    dados = np.loadtxt("./src/prog2021_formatado/L13.csv", delimiter=" ")[:qtd_Dados, 0] # Lê os dados diretamente com numpy
    dados = dados.reshape(-1, 1666)  # Faz o reshape diretamente com numpy

    # Obter a classificação
    resultado = getClasse(dados)
    print(f"{resultado}")

if __name__ == "__main__":
    main()