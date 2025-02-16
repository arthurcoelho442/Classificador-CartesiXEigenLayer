from sklearn.preprocessing import MinMaxScaler
import tflite_runtime.interpreter as tflite
import pandas as pd
import numpy as np

# Carregar modelo TFLite
interpreter = tflite.Interpreter(model_path="./backup/classificador.tflite")
interpreter.allocate_tensors()

# Obter informações do modelo
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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

        # Encontrar picos sem SciPy
        derivada = np.diff(amplet)
        pontos = np.where((derivada[:-1] > 0) & (derivada[1:] < 0))[0]

        peak_x = np.abs(freqs[pontos])[:qtd_Peaks]
        peak_y = np.abs(amplet[pontos])[:qtd_Peaks]

        lista = list(peak_x) + list(peak_y)
        L.append(lista)
        
        scaler = MinMaxScaler(feature_range=(0,1))
        
    return scaler.fit_transform(pd.DataFrame(L)) #type: ignore

def getClasse(dados):
    harmonicos_normalizados = getHarmonicos(dados)

    classe = pd.DataFrame()
    for harm in harmonicos_normalizados:
        interpreter.set_tensor(input_details[0]['index'], [harm.astype(np.float32)])
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])
    
        classe = pd.concat([classe, pd.DataFrame(predictions.round(decimals = 2), columns=[10, 13, 14, 15])])
    
    print(classe)
    coluna_maior  = classe.idxmax(axis=1) # pega coluna com valor mais proximo de 1
    # frequência de cada coluna
    frequencia_colunas = coluna_maior.value_counts()
    # Coluna que aparece mais vezes
    coluna_mais_frequente = frequencia_colunas.idxmax()

    print("Coluna que aparece mais vezes como a maior:", coluna_mais_frequente)
    print("Frequência das colunas:\n", frequencia_colunas) # pega coluna com valor mais proximo de 1
    return coluna_mais_frequente