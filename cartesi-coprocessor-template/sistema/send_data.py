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
    if not web3.isConnected():
        print("Erro ao conectar no nó Ethereum.")
        return

    # Configurações do contrato
    contract_address = web3.toChecksumAddress("0xSeuEnderecoDoContrato")  # Substitua pelo endereço do seu contrato
    contract_abi = json.loads('''
    [
        {
            "inputs": [
                {
                    "internalType": "uint256[]",
                    "name": "currents",
                    "type": "uint256[]"
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
    account_address = web3.toChecksumAddress("0xSeuEnderecoDaConta")  # Substitua pelo seu endereço
    private_key = "sua_chave_privada_aqui"  # Substitua pela sua chave privada (mantenha-a segura!)
    nonce = web3.eth.get_transaction_count(account_address)

    # Leitura e processamento do arquivo CSV
    try:
        df = pd.read_csv(filepath, delimiter="  ", header=None, engine='python')
        data = df.values.flatten()
    except Exception as e:
        print("Erro ao ler o arquivo CSV:", e)
        return

    batch_size = 1666  # 1 segundo de dados
    total_values = len(data)
    total_batches = total_values // batch_size
    print(f"Total de valores lidos: {total_values}. Batches a enviar: {total_batches}.")

    # Intervalo de envio (5 segundos)
    interval = 5

    # Envio contínuo dos dados, batch por batch
    for batch_index in range(total_batches):
        start_time = time.time()

        # Extrai o batch de 1.666 valores
        batch_data = data[batch_index * batch_size: (batch_index + 1) * batch_size]
        if len(batch_data) != batch_size:
            print(f"Batch {batch_index + 1} incompleto (tamanho: {len(batch_data)}). Pulando...")
            continue

        try:
            currents_list = [int(x) for x in batch_data]
        except Exception as e:
            print(f"Erro ao converter valores do batch {batch_index + 1}: {e}")
            continue

        # Obtém o timestamp atual para este batch
        timestamp_value = int(time.time())
        print(f"Enviando batch {batch_index + 1}/{total_batches} com timestamp {timestamp_value}.")

        # Constrói e envia a transação
        try:
            tx = contract.functions.sendData(currents_list, timestamp_value).buildTransaction({
                'chainId': 1337,           # Ajuste para sua rede (ex.: 1 para Mainnet, 3 para Testnet, 1337 para rede local)
                'gas': 5000000,            # Ajuste o gas conforme necessário
                'gasPrice': web3.toWei('20', 'gwei'),
                'nonce': nonce,
            })
            signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"Batch {batch_index + 1} enviado. Tx hash: {web3.toHex(tx_hash)}")
            nonce += 1  # Incrementa o nonce para a próxima transação
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