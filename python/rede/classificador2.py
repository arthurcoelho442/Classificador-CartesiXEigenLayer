from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from scipy import signal
import tensorflow as tf
import pandas as pd
import numpy as np

tf.get_logger().setLevel('ERROR')

# Carregar o modelo
modelo_carregado = load_model('./backup/classificador.h5')

def getHarmonicos(dados, qtd_Peaks=7):
    frequencia  = 60  # Hz
    T           = 1 / frequencia
    amostras    = int(T * 10**5)
    L = []
    for i in range(0, len(dados)):
        df = dados.iloc[i,:].transpose()

        # Faz a transformada rápida de fourrier
        fft = np.fft.fft(df)

        # Faz a transformada rápida de fourrier
        fast = np.fft.fftfreq(amostras, T)

        # Seleciona a primeira metade da sequência e normaliza as amplitudes pelo número de amostras (divide por N)
        freqs = fast[:amostras//2]

        # Pega amplitudes
        amplet = np.abs(fft)[:amostras//2] / amostras
        amplet = np.log10(amplet)*20

        pontos = signal.argrelextrema(amplet, np.greater)
        pontos = pontos[0]

        peak_x = list(np.abs(freqs[pontos]))
        peak_y = list(np.abs(amplet[pontos]))

        lista = []
        for j in range(0, qtd_Peaks, 1):
            lista.append(peak_x[j])

        for j in range(0, qtd_Peaks, 1):
            lista.append(peak_y[j])

        L.append(lista)
        
        scaler = MinMaxScaler(feature_range=(0,1))
    return scaler.fit_transform(pd.DataFrame(L)) #type: ignore

def getClasse(dados):
    harmonicos_normalizados = getHarmonicos(dados)
    
    predictions = modelo_carregado.predict(harmonicos_normalizados)
    predictions = predictions.round(decimals = 2)
    classe = pd.DataFrame(predictions.round(decimals = 2), columns=[10, 13, 14, 15])
    print(classe)
    
    coluna_maior  = classe.idxmax(axis=1) # pega coluna com valor mais proximo de 1
    # frequência de cada coluna
    frequencia_colunas = coluna_maior.value_counts()
    # Coluna que aparece mais vezes
    coluna_mais_frequente = frequencia_colunas.idxmax()

    print("Coluna que aparece mais vezes como a maior:", coluna_mais_frequente)
    print("Frequência das colunas:\n", frequencia_colunas) # pega coluna com valor mais proximo de 1
    return coluna_mais_frequente