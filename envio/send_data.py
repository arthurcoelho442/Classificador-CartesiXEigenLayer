import time
import json
import sys
import pandas as pd
from web3 import Web3

def main():
    # Verifica se o nome do arquivo foi passado como argumento
    if len(sys.argv) < 2:
        print("Uso: python send_data.py <nome_do_arquivo_sem_extensao>")
        return

    filename = sys.argv[1]
    filepath = f"./src/prog2021/{filename}.csv"

    # Conectar ao nó Ethereum
    provider_url = "http://127.0.0.1:8545"  # Ajuste conforme seu provider
    web3 = Web3(Web3.HTTPProvider(provider_url))
    if not web3.is_connected():
        print("Erro ao conectar no nó Ethereum.")
        return

    # Configurações do contrato
    contract_address = web3.to_checksum_address("0xBEc49fA140aCaA83533fB00A2BB19bDdd0290f25")  # Substitua pelo endereço do seu contrato
    contract_abi = json.loads('''
    [
        {
            "inputs": [
                {
                    "internalType": "int256[]",
                    "name": "currents",
                    "type": "int256[]"
                },
                {
                    "internalType": "uint256",
                    "name": "timestamp",
                    "type": "uint256"
                }
            ],
            "name": "sendData",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
    ''')
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Configurações da conta que enviará as transações
    account_address = web3.to_checksum_address("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")  # Substitua pelo seu endereço

    # Leitura e processamento do arquivo CSV
    try:
        df = pd.read_csv(filepath, delimiter="  ", header=None, engine='python').iloc[:, 0] * 10000
        dados = df.astype(int).tolist()
    except Exception as e:
        print("Erro ao ler o arquivo CSV:", e)
        return

    batch_size = 4998  # 1 segundo de dados
    total_values = len(dados)
    total_batches = total_values // batch_size
    print(f"Total de valores lidos: {total_values}. Batches a enviar: {total_batches}.")

    # Intervalo de envio (5 segundos)
    interval = 10 # AUMENTAR O INTERVALO

    # Envio contínuo dos dados, batch por batch
    for batch_index in range(total_batches):
        start_time = time.time()

        # Extrai o batch de 1.666 valores
        currents_list = dados[batch_index * batch_size: (batch_index + 1) * batch_size]
        if len(currents_list) != batch_size:
            print(f"Batch {batch_index + 1} incompleto (tamanho: {len(currents_list)}). Pulando...")
            continue

        # Obtém o timestamp atual para este batch
        timestamp_value = int(time.time())
        print(f"Enviando batch {batch_index + 1}/{total_batches} com timestamp {timestamp_value}.")

        # Constrói e envia a transação
        try:
            web3.eth.default_account = web3.eth.accounts[0]
            tx = contract.functions.sendData(currents_list, timestamp_value).transact({"from": web3.eth.default_account})
            
        except Exception as e:
            print(f"Erro ao enviar o batch {batch_index + 1}: {e}")


        # Aguarda o tempo restante para completar o intervalo de 5 segundos
        elapsed = time.time() - start_time
        if elapsed < interval:
            sleep_time = interval - elapsed
            print(f"Batch {batch_index + 1} enviado. Aguardando {sleep_time:.3f} segundos para o próximo envio.")
            time.sleep(sleep_time)
        else:
            print(f"Batch {batch_index + 1} enviado. Tempo decorrido: {elapsed:.3f} segundos.")

        
    print("Envio dos dados concluído.")

if __name__ == "__main__":
    main()