from os import environ
import logging
import requests
import tflite_runtime.interpreter as tflite
from scipy import signal
import pandas as pd
import numpy as np
from eth_abi import encode

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

# Carregar modelo TFLite
interpreter = tflite.Interpreter(model_path="./classificador.tflite")
interpreter.allocate_tensors()

# Obter informações do modelo
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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
        df = pd.Series(dados[i]) / 10000

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
    return min_max_scale(L)

def getClasse(dados):
    harmonicos_normalizados = getHarmonicos(dados)    
    classe = pd.DataFrame()
    for harm in harmonicos_normalizados:
        interpreter.set_tensor(input_details[0]['index'], [harm.astype(np.float32)])
        interpreter.invoke()
        predictions = interpreter.get_tensor(output_details[0]['index'])
    
        classe = pd.concat([classe, pd.DataFrame(predictions.round(decimals = 2), columns=[10, 13, 14, 15])])
    
    print(classe)
    coluna_maior = classe.idxmax(axis=1)
    coluna_mais_frequente = coluna_maior.value_counts().idxmax()
    
    return int(coluna_mais_frequente)
    
def emit_notice(data):
    notice_payload = {"payload": data["payload"]}
    response = requests.post(rollup_server + "/notice", json=notice_payload)
    if response.status_code == 200 or response.status_code == 201:
        logger.info(f"Notice emitted successfully with data: {data}")
    else:
        logger.error(f"Failed to emit notice with data: {data}. Status code: {response.status_code}")

# Função para decodificar uint256[] manualmente
def decode_int256_array(payload_bytes):
    int_size = 32  # 32 bytes por int256
    num_elements = len(payload_bytes) // int_size  # Número de elementos no array
    return [int.from_bytes(payload_bytes[i * int_size: (i + 1) * int_size], "big", signed=True) for i in range(num_elements)]

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    payload_hex = data['payload']
    
    try:
        # Decodificando o payload hexadecimal para bytes
        payload_bytes = bytes.fromhex(payload_hex[2:])
        
        # Decodificando os dados (supondo que seja um vetor de uint256)
        decoded_data = decode_int256_array(payload_bytes)

        decoded_data = decoded_data[2:]

        # Verificando se o número de elementos é divisível por 1666
        if len(decoded_data) % 1666 != 0:
            logger.error("O número de elementos não é divisível por 1666.")
            return "reject"

        # Criando uma lista de listas (reshape manual)
        dados = pd.DataFrame(decoded_data).values.reshape(-1,1666).tolist()
        
        # Calculando a classe com a função getClasse
        classe = getClasse(dados)

        if classe is None:
            return "reject"

        # Calculando a média dos dados
        mean_current = int(sum(decoded_data) / len(decoded_data))

        # Convertendo a resposta para hexadecimal
        # ABI encode the data
        encoded_data = encode(
            ['int256', 'int256'],
            [classe, mean_current]
        )
        
        # Convert to hex and emit notice
        hex_data = "0x" + encoded_data.hex()

        # Emitindo o aviso com o resultado
        payload = {"payload": hex_data}

        emit_notice(payload)

        return "accept"
    
    except Exception as error:
        print(f"Error processing payload: {error}")
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