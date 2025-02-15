import pandas as pd
from rede.classificador import getClasse

# Frequencia utilizada
frequencia  = 60  # Hz
# Periodo
T           = 1 / frequencia  # quantidade de amostras por segundo
# Quantidade de amostras
amostras    = int(T * 10**5)
# Quantidade de dados totais
aux         = 10
qtd_Dados   = aux * amostras

# Ler os dados
dados = pd.read_csv("./src/prog2021/L6.csv", delimiter="  ", header=None, engine='python').iloc[:qtd_Dados, 1:2]
dados  = pd.DataFrame(dados.values.reshape(-1,1666))

resultado = getClasse(dados, amostras, T)
print(resultado)