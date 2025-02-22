from os import environ
import logging
import requests
from eth_utils import decode_hex
from eth_abi import decode_abi

import tflite_runtime.interpreter as tflite
from sklearn.preprocessing import MinMaxScaler
from scipy import signal
import pandas as pd
import numpy as np

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

# Carregar modelo TFLite
interpreter = tflite.Interpreter(model_path="./backup/classificador.tflite")
interpreter.allocate_tensors()

# Obter informações do modelo
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

scaler = MinMaxScaler(feature_range=(0,1))

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
        
    return scaler.fit_transform(pd.DataFrame(L)) #type: ignore

def getClasse(dados):
    harmonicos_normalizados = getHarmonicos(dados)

    classe = pd.DataFrame()
    for harm in harmonicos_normalizados:
        interpreter.set_tensor(input_details[0]['index'], [harm.astype(np.float32)])
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])
        
        classe = pd.concat([classe, pd.DataFrame(predictions.round(2), columns=[10, 13, 14, 15])])
    
    print(classe)
    
    coluna_maior  = classe.idxmax(axis=1) # pega coluna com valor mais proximo de 1
    # frequência de cada coluna
    frequencia_colunas = coluna_maior.value_counts()
    # Coluna que aparece mais vezes
    coluna_mais_frequente = frequencia_colunas.idxmax()

    print("Coluna que aparece mais vezes como a maior:", coluna_mais_frequente)
    print("Frequência das colunas:\n", frequencia_colunas) # pega coluna com valor mais proximo de 1
    return coluna_mais_frequente

# Função para emitir o aviso
def emit_notice(data):
    notice_payload = {"payload": data["payload"]}
    response = requests.post(rollup_server + "/notice", json=notice_payload)
    if response.status_code == 200 or response.status_code == 201:
        logger.info(f"Notice emitted successfully with data: {data}")
    else:
        logger.error(f"Failed to emit notice with data: {data}. Status code: {response.status_code}")

# Função para converter os dados de uint256 para float (dividindo por 10000)
def convert_to_float(data, scale_factor=10000):
    return np.array(data) / scale_factor

# Função para lidar com o payload recebido, processando os dados e aplicando o reshape
def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    payload_hex = data['payload']
    
    try:
        # Decodificando o payload hexadecimal para bytes
        payload_bytes = bytes.fromhex(payload_hex[2:])
        
        # Decodificando os dados (supondo que seja um vetor de uint256)
        decoded_data = decode_abi(['uint256[]'], payload_bytes)[0]

        # Convertendo os valores para float (dividindo por 10000)
        currents_in_float = convert_to_float(decoded_data)

        # Verificando se o número de elementos é divisível por 1666
        if len(currents_in_float) % 1666 != 0:
            logger.error("O número de elementos não é divisível por 1666.")
            return "reject"

        # Criando o array numpy e aplicando o reshape
        dados = pd.DataFrame(currents_in_float.reshape(-1,1666))
        
        # Calculando a classe com a função getClasse
        classe = getClasse(dados)

        # Calculando a média dos dados
        mean_current = int(dados.mean().mean() * 10000)

        # Emitindo o aviso com o resultado
        payload = {"payload": f"{classe},{mean_current}"}
        emit_notice(payload)

        return "accept"
    
    except Exception as error:
        logger.error(f"Erro ao processar dados: {error}")
        return "reject"

handlers = {
    "advance_state": handle_advance,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])