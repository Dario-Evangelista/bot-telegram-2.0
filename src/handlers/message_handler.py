import json
import logging
logging.basicConfig(filename='src/logs/errors.log', level=logging.ERROR)

def get_commands_and_messages(token):
    try:
        with open('src/handlers/message.json', 'r') as file:
            data = json.load(file)
        commands_and_messages = {entry["comando"]: entry["message"] for entry in data if entry["token"] == token}
        
        return commands_and_messages
    except Exception as e:
        logging.error(f"Erro ao carregar tokens: {e}")
        return {}

def response_command(token, command):
    commands_and_messages = get_commands_and_messages(token)
    if command in commands_and_messages:
        return command, commands_and_messages[command]
    else:
        print(f"Comando '{command}' não encontrado para o token fornecido.")

