from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from scipy import signal
import tensorflow as tf
import pandas as pd
import numpy as np

tf.get_logger().setLevel('ERROR')

# Inicializa a API Flask
app = Flask(__name__)

# Carregar o modelo
modelo_carregado = load_model('./classificador.h5')
scaler = MinMaxScaler(feature_range=(0, 1))

frequencia = 60  # Hz
T = 1 / frequencia
amostras = int(T * 10**5)

def min_max_scale(data, feature_range=(0, 1)):
    """
    Normaliza os dados para um intervalo específico usando Min-Max Scaling.

    Parâmetros:
        data (array-like): Dados de entrada para normalização.
        feature_range (tuple): Intervalo desejado (mínimo, máximo), padrão (0,1).

    Retorna:
        np.ndarray: Dados normalizados no intervalo especificado.
    """
    data = np.asarray(data, dtype=np.float64)  # Converter para numpy array
    min_val, max_val = np.min(data), np.max(data)  # Encontrar min e max
    a, b = feature_range  # Novo intervalo

    if max_val == min_val:
        return np.full_like(data, (a + b) / 2)  # Evitar divisão por zero

    return a + ((data - min_val) * (b - a)) / (max_val - min_val)

def getHarmonicos(dados, qtd_Peaks=7):
    L = []
    for i in range(len(dados)):
        df = pd.Series(dados[i])

        fft = np.fft.fft(df)
        fast = np.fft.fftfreq(amostras, T)
        freqs = fast[:amostras//2]
        amplet = np.abs(fft)[:amostras//2] / amostras
        amplet = np.log10(amplet) * 20

        pontos = signal.argrelextrema(amplet, np.greater)[0]
        peak_x = list(np.abs(freqs[pontos]))[:qtd_Peaks]
        peak_y = list(np.abs(amplet[pontos]))[:qtd_Peaks]

        lista = peak_x + peak_y
        L.append(min_max_scale(lista))
    return pd.DataFrame(L)

def getClasse(dados):
    harmonicos_normalizados = getHarmonicos(dados)
    predictions = modelo_carregado.predict(harmonicos_normalizados)
    predictions = predictions.round(decimals=2)
    
    classe = pd.DataFrame(predictions, columns=[10, 13, 14, 15])
    coluna_maior = classe.idxmax(axis=1)
    coluna_mais_frequente = coluna_maior.value_counts().idxmax()
    
    return int(coluna_mais_frequente)

@app.route('/classificar', methods=['POST'])
def classificar():
    try:
        dados = request.json.get("dados", [])
        if not dados:
            return jsonify({"erro": "Nenhum dado fornecido."}), 400
        
        # Converter para DataFrame e dividir por 1000
        df = pd.DataFrame(dados) / 10000
        print(df)
        # Converter de volta para lista de listas para compatibilidade com `getClasse`
        dados_processados = df.values.tolist()
        
        resultado = getClasse(dados_processados)
        return jsonify({"classe": resultado})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)