from os import environ
import logging
import requests
import json

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

# URL da API externa
api_url = "http://host.docker.internal:5000/getClasse"

def getClasse(dados):
    # Envia os dados para a API externa e recebe a classe
    response = requests.post(api_url, json={"dados": dados})
    if response.status_code == 200:
        return response.json()["classe"]
    else:
        logger.error(f"Erro ao chamar API externa: {response.status_code}")
        return None
    
def emit_notice(data):
    notice_payload = {"payload": data["payload"]}
    response = requests.post(rollup_server + "/notice", json=notice_payload)
    if response.status_code == 200 or response.status_code == 201:
        logger.info(f"Notice emitted successfully with data: {data}")
    else:
        logger.error(f"Failed to emit notice with data: {data}. Status code: {response.status_code}")

# Função para decodificar uint256[] manualmente
def decode_uint256_array(payload_bytes):
    uint_size = 32  # 32 bytes por uint256
    num_elements = len(payload_bytes) // uint_size  # Número de elementos no array
    return [int.from_bytes(payload_bytes[i * uint_size: (i + 1) * uint_size], "big") for i in range(num_elements)]


def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    payload_hex = data['payload']
    
    try:
        # Decodificando o payload hexadecimal para bytes
        payload_bytes = bytes.fromhex(payload_hex[2:])
        
        # Decodificando os dados (supondo que seja um vetor de uint256)
        decoded_data = decode_uint256_array(payload_bytes)

        # Verificando se o número de elementos é divisível por 1666
        if len(decoded_data) % 1666 != 0:
            logger.error("O número de elementos não é divisível por 1666.")
            return "reject"

        # Criando uma lista de listas (reshape manual)
        dados = [decoded_data[i:i + 1666] for i in range(0, len(decoded_data), 1666)]
        
        # Calculando a classe com a função getClasse
        classe = getClasse(dados)

        if classe is None:
            return "reject"

        # Calculando a média dos dados
        mean_current = int(sum(sum(sublist) for sublist in dados) / len(decoded_data))

        # Emitindo o aviso com o resultado
        payload = {"payload": f"{classe},{mean_current}"}
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
