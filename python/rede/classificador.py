import tflite_runtime.interpreter as tflite
import numpy as np

# Carregar modelo TFLite
interpreter = tflite.Interpreter(model_path="./backup/classificador.tflite")
interpreter.allocate_tensors()

# Obter informações do modelo
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Função de normalização MinMax ajustada para evitar NaN
def normalize_minmax(data, feature_range=(0, 1)):
    min_val, max_val = feature_range
    data_min = np.min(data, axis=0)
    data_max = np.max(data, axis=0)

    # Para evitar divisão por zero, substituímos os casos de diferença zero por 1 (não afeta a normalização)
    diff = data_max - data_min
    diff[diff == 0] = 1  # Quando a diferença é zero, substituímos por 1

    # Normalização
    normalized_data = (data - data_min) / diff
    normalized_data = normalized_data * (max_val - min_val) + min_val
    
    return normalized_data

def getHarmonicos(dados, qtd_Peaks=7):
    frequencia  = 60  # Hz
    T           = 1 / frequencia
    amostras    = int(T * 10**5)
    L = []
    for i in range(0, len(dados)):
        df = dados[i, :].transpose()

        # Faz a transformada rápida de fourrier
        fft = np.fft.fft(df)

        # Faz a transformada rápida de fourrier
        fast = np.fft.fftfreq(amostras, T)

        # Seleciona a primeira metade da sequência e normaliza as amplitudes pelo número de amostras (divide por N)
        freqs = fast[:amostras // 2]

        # Pega amplitudes
        amplet = np.abs(fft)[:amostras // 2] / amostras
        amplet = np.log10(amplet) * 20

        # Encontrar picos sem SciPy
        derivada = np.diff(amplet)
        pontos = np.where((derivada[:-1] > 0) & (derivada[1:] < 0))[0]

        peak_x = np.abs(freqs[pontos])[:qtd_Peaks]
        peak_y = np.abs(amplet[pontos])[:qtd_Peaks]

        lista = np.concatenate((peak_x, peak_y))
        L.append(lista)
    return normalize_minmax(np.array(L))  # Agora a lista é convertida para np.array

def getClasse(dados):
    harmonicos_normalizados = getHarmonicos(dados)
    
    classe = []
    for harm in harmonicos_normalizados:
        interpreter.set_tensor(input_details[0]['index'], [harm.astype(np.float32)])
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])
        
        classe.append(predictions.round(2))

    classe = np.array(classe)
    classe_2d = classe.squeeze()
    
    print(classe_2d)
    
    label = [10, 13, 14, 15]
    coluna_maior = np.argmax(classe_2d, axis=1)  # pega a coluna com valor mais próximo de 1
    # Frequência de cada coluna
    frequencia_colunas = np.bincount(coluna_maior)
    # Coluna que aparece mais vezes
    coluna_mais_frequente = np.argmax(frequencia_colunas)

    frequencia_colunas = { l: freq for l, freq in zip(label, frequencia_colunas)}
    
    print("Coluna que aparece mais vezes como a maior:", label[coluna_mais_frequente])
    print(f"Frequência das colunas:\n{frequencia_colunas}")  # pega a coluna com valor mais próximo de 1
    return label[coluna_mais_frequente]