from os import environ
import logging
import requests
import json
import pandas as pd
from eth_utils import decode_hex
from eth_abi import decode_abi
from ..sistema.rede.classificador import getClasse

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

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
    return [x / scale_factor for x in data]

# Função para lidar com o payload recebido, processando os dados e aplicando o reshape
def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    payload_hex = data['payload']
    
    try:
        # Decodificando o payload hexadecimal para bytes
        payload_bytes = bytes.fromhex(payload_hex[2:])
        
        # Decodificando os dados (supondo que seja um vetor de uint256)
        decoded_data = decode_abi(['uint256[]'], decode_hex(payload_bytes))[0]
        
        # Convertendo os valores para float (dividindo por 10000)
        currents_in_float = convert_to_float(decoded_data)

        # Verificando se o número de elementos é divisível por 1666
        if len(currents_in_float) % 1666 != 0:
            logger.error("O número de elementos não é divisível por 1666.")
            return "reject"

        # Criando um DataFrame com os dados e aplicando o reshape diretamente
        dados = pd.DataFrame(currents_in_float)

        # Aplicando reshape no DataFrame
        df = pd.DataFrame(dados.values.reshape(-1, 1666))
        
        # Calculando a classe com a função getClasse
        classe = getClasse(df)

        # Calculando a média dos dados
        mean_current = df.mean(axis=1).mean() * 10000

        # Emitindo o aviso com o resultado
        payload = {"payload": f"{classe},{int(mean_current)}"}
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