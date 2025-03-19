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
        L.append(lista)
    return scaler.fit_transform(pd.DataFrame(L))

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
    app.run(host='127.0.0.1', port=5004, debug=True)