import requests
import json
import re
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import logging
from src.handlers.message_handler import response_command

logging.basicConfig(filename='src/logs/errors.log', level=logging.ERROR)

class Message():
    def __init__(self, token) -> None:
        self.token = token
        self.url = f"https://api.telegram.org/bot{token}/"

    def get_update(self, data):
        requests.get(self.url + 'getUpdates', data={'offset': data['update_id'] + 1})

    def get_messages(self, data):
        command_reponse, msg_reponse = response_command(self.token, data['message']['text'])
        if data['message']['text'] == command_reponse:
            requests.post(self.url + 'SendMessage', data={'chat_id': data['message']['chat']['id'], 'text': str(msg_reponse)})

    def get_message(self,data,msg):
        requests.post(self.url + 'SendMessage', data={'chat_id': data['message']['chat']['id'], 'text': str(msg)})
    
    def get_message_client(self,client,msg):
        requests.post(self.url + 'SendMessage', data={'chat_id': client, 'text': str(msg)})
            
    def send_markup(self,data, command, keyboard, msg):
        reply_markup = keyboard
        if data['message']['text'] == command:
            requests.post(self.url + 'sendMessage', data={'text': msg,
                                                             'chat_id': data['message']['chat']['id'],
                                                             'reply_markup': json.dumps(reply_markup),
                                                             'disable_web_page_preview': 'true'})
            
    def get_file(self, data, file):
        aqv = {'png': {'metodo': 'sendPhoto', 'send': 'photo'},
                'jpg': {'metodo': 'sendPhoto', 'send': 'photo'}}
        file_format = 'jpg' if '.jpg' in file else 'png' if '.png' in file else None
        if file_format:
            return requests.get(self.url + aqv[file_format]['metodo'], params={'chat_id': data['message']['chat']['id']},
                                files={aqv[file_format]['send']: open(file, 'rb')}).text
        else:
            return "Formato de arquivo inválido."
            
    def get_address_from_cep(self, cep):
        url = f'https://viacep.com.br/ws/{cep}/json/'
        try:
            response = requests.get(url)
            data = response.json()
            if 'erro' not in data:
                endereco = {
                    'logradouro': data['logradouro'],
                    'bairro': data['bairro'],
                    'cidade': data['localidade'],
                    'estado': data['uf']
                }
                return endereco
            else:
                return None
        except Exception as e:
            print(f"Ocorreu um erro ao obter o endereço do CEP {cep}: {str(e)}")
            return None

    def obter_coordenadas_por_endereco(self, endereco):
        endereco_formatado = f"{endereco['logradouro']}, {endereco['bairro']}, {endereco['cidade']}, {endereco['estado']}"
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={endereco_formatado}&key=AIzaSyDVy2Rk6kaaiJipwUIG7dFmHYAiB9MrWjU'
        try:
            response = requests.get(url)
            data = response.json()
            if data['status'] == 'OK':
                latitude = data['results'][0]['geometry']['location']['lat']
                longitude = data['results'][0]['geometry']['location']['lng']
                return latitude, longitude
            else:
                return None, None
        except Exception as e:
            print(f"Ocorreu um erro ao obter coordenadas para o endereço {endereco_formatado}: {str(e)}")
            return None, None

    def calcular_distancia_entre_coordenadas(self, coordenadas1, coordenadas2):
        distancia = geodesic(coordenadas1, coordenadas2).kilometers
        return distancia

    def calcular_frete_entre_ceps(self, cep1, cep2):
        endereco1 = self.get_address_from_cep(cep1)
        endereco2 = self.get_address_from_cep(cep2)

        if endereco1 is not None and endereco2 is not None:
            coordenadas1 = self.obter_coordenadas_por_endereco(endereco1)
            coordenadas2 = self.obter_coordenadas_por_endereco(endereco2)
            if coordenadas1 is not None and coordenadas2 is not None:
                distancia = self.calcular_distancia_entre_coordenadas(coordenadas1, coordenadas2)
                if distancia <= 1:
                    valor_frete = 1 * 3
                else:
                    valor_frete = distancia * 3
                return valor_frete
            else:
                return "Não foi possível obter as coordenadas geográficas de pelo menos um dos endereços."
        else:
            return "Não foi possível obter o endereço de pelo menos um dos CEPs."

    def identificar_cep(self,mensagem):
        padrao_cep = r'\b\d{5}-\d{3}\b'
        padrao_cep2 = r'\b\d{8,9}\b'
        match = re.search(padrao_cep, mensagem)
        match2 = re.search(padrao_cep2, mensagem)
        
        if match:
            return True, match.group(0)  
        elif match2:
            return True, match2.group(0)
        else:
            return False, None
        

    def get_message_add(self, data):
        user_id = data['message']['from']['id']
        chat_id = -1002046950406
        return user_id, chat_id

    def remover_membro_do_grupo(self, data):
        data=data
        token = self.token
        user_id, chat_id = self.get_message_add(data)
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

    def add_membro_do_grupo(self, data):
        data=data
        token = self.token
        user_id, chat_id = self.get_message_add(data)
        chat_id = '-1002046950406'
        url = f"https://api.telegram.org/bot{token}/addChatMember"
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


    



    