import json
import threading
import time
from src import config, utils, core
import logging

logging.basicConfig(filename='src/logs/errors.log', level=logging.ERROR)

def token_file():
    try:
        with open('src/data/token.json', 'r') as arquivo:
            dados = json.load(arquivo)    
        tokens = [valor.get('token') for valor in dados.values()]
        return tokens
    except Exception as e:
        logging.error(f"Erro ao carregar tokens: {e}")
        return []
    
def main():
    tokens = token_file()

    for token in tokens:
        temp = core.Run(token)
        threading.Thread(target=temp.processar_mensagens, daemon=True).start()
    while True:
        time.sleep(1)
if __name__ == "__main__":
    main()