import requests

def enviar_mensagem_de_boas_vindas(token, user_id):
    chat_id = -1002046950406
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    mensagem = "Bem-vindo ao grupo! Esperamos que você se divirta aqui."
    params = {
        'chat_id': chat_id,
        'text': mensagem,
        'reply_to_message_id': user_id  # Responder à mensagem do usuário que acabou de entrar no grupo
    }
    response = requests.post(url, params=params)
    if response.ok:
        print("Mensagem de boas-vindas enviada com sucesso!")
    else:
        print("Falha ao enviar mensagem de boas-vindas.")
        print("Código de status:", response.status_code)
        print("Resposta:", response.text)


def remover_membro_do_grupo(token, chat_id, user_id):
    url = f"https://api.telegram.org/bot{token}/kickChatMember"
    params = {
        'chat_id': chat_id,
        'user_id': user_id
    }
    response = requests.post(url, params=params)
    if response.ok:
        print(f"Usuário {user_id} removido do grupo {chat_id} com sucesso!")
    else:
        print(f"Falha ao remover o usuário {user_id} do grupo {chat_id}.")
        print("Código de status:", response.status_code)
        print("Resposta:", response.text)

# Exemplo de uso
if __name__ == "__main__":
    token = '6729902739:AAGdX2ekGn4GeIjx7tAGxA4quCjCWX_Fo4I'
    chat_id = '-1002046950406'
    user_id = '7137868694'
    remover_membro_do_grupo(token, chat_id, user_id)


