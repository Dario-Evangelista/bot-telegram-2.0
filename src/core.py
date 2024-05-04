import requests
import json
import logging
from src.utils import Message
import time

class Run(Message):
    def __init__(self, token):
        super().__init__(token)
        self.token = token
        self.initial = 1

    def processar_mensagens(self):
        text = ''
        local = 0
        endereco = False
        end = 1
        cep1 = ''
        cep2 = ''
        latitude = ''
        group = 1
        while True:
            try:
                x = ''
                while 'result' not in x:
                    try:
                        x = json.loads(requests.get(self.url + 'getUpdates').text)
                    except Exception as e:
                        x = ''
                        if 'Failed to establish a new connection' in str(e):
                            print('Perda de conexão')
                        else:
                            print('Erro desconhecido: ' + str(e))

                if len(x['result']) > 0:
                    for data in x['result']:
                        x=json.dumps(data, indent=1)
                        print(f"Atualizações para o bot {self.token}: {x}")
                        message = Message(self.token)
                        message.get_update(data)
                        print(json.dumps(data, indent=1))
                        
                        data_message = data['message']

                        if 'text' in data_message:
                            text= data_message['text']

                        if text and self.initial == 1:
                            self.initial = 0
                            reply_markup = {
                                'keyboard': [[{'text':'Conhecer recursos do Bot'}],
                                            [{'text':'Fazer um pedido'}],
                                ],           
                                'one_time_keyboard': True,
                                'resize_keyboard': True,
                            }
                            message.send_markup(data,text,reply_markup,"Olá! Seja muito bem-vindo ao nosso bot! Estamos aqui para ajudar e proporcionar uma experiência incrível. Sinta-se à vontade.")

                        elif text == 'Conhecer recursos do Bot' or text == "Voltar" or text == "/voltar":
                            reply_markup = {
                                'keyboard': [
                                            [{'text':'Localização'}],
                                            [{'text':'Envio de Conteúdos'}],
                                            [{'text':'Administrar Grupos'}],
                                            [{'text':'Falar com atendete'}],
                                            [{'text':'Voltar'}],
                                ],           
                                'one_time_keyboard': True,
                                'resize_keyboard': True,
                            }
                            group = 1
                            message.send_markup(data,text,reply_markup,"""
Recurso do Bot:
Localização, ele consegue calcular frete 
Receber Pagamentos e autenticar
Cria uma lista de pagamentos mensais
Envio de Conteúdos
Administrar Grupos
Extrair pessoas de outros Grupos
e pode personalizar ele do seu jeito""")
                            
                        if text.lower() in ["fazer um pedido", "/fazer um pedido", "falar com atendete", "/falarcomatendete"]:                            
                            message.get_message(data, "Para conversar com nossos atendentes, é só mandar uma mensagem para o número 11971805330 ou ir no link: https://api.whatsapp.com/send?phone=5511971805330&text=Ol%C3%A1%20quero%20um%20or%C3%A7amento%20do%20Bot%20do%20telegram")
                            cliente_id = data['message']['chat']['id']
                            with open("data/client.txt", 'a') as arquivo:
                                arquivo.write(str(cliente_id) + '\n')


                        elif text == 'Localização':
                            local = 1
                            message.get_message(data, "Digite o Cep")
                            message.get_message(data, "caso queira voltar só digitar /voltar")

                        elif text and local == 1:
                            cep_amaz = []
                            loc = text
                            true, cep = message.identificar_cep(loc)
                            if true:
                                if endereco:
                                    address = message.get_address_from_cep(cep)
                                    if address:
                                        message.get_message(data, f"Segundo endereço é: {address}")
                                        cep2 = cep
                                        message.get_message(data, "Vamos supor que o valor de km seria R$ 3,00")
                                        result = message.calcular_frete_entre_ceps(cep1, cep2)
                                        message.get_message(data, f"O valor do frete entre os CEPs {cep1} e {cep2} é de R$ {result:.2f}")
                                        endereco=False

                                address = message.get_address_from_cep(cep)
                                if address and end == 1:
                                    cep1 = cep
                                    end = 0
                                    message.get_message(data, f"Primeiro endereço é: {address}")
                                    message.get_message(data, "Digite o Segundo Cep")
                                    endereco = True
                                else:
                                    message.get_message(data, "Cep não localizado, digite novamente")
                            else:
                                message.get_message(data, "Não conseguir identificar o Cep")

                        elif 'location' in data['message'] and local == 1:
                            location = data['message']['location']
                            if latitude:
                                latitude1 = location['latitude']
                                longitude1 = location['longitude']
                            else:
                                latitude = location['latitude']
                                longitude = location['longitude']

                            end = 0

                        elif text == 'Envio de Conteúdos':
                            message.get_file(data, 'src/data/p.jpg')
                            message.get_message(data, 'Aqui o nosso bot consegue enviar media para grupos ou pessoa em particular, apartir de assinatura ou não')
                            message.get_file(data, 'src/data/y.jpg')
                            message.get_message(data, 'recursos podem ser personalizado do seu jeito, se gostou e quer saber mais ==> /falarcomatendente')

                        elif text == 'Administrar Grupos' and group == 1:
                            client = data['message']['chat']['id']
                            message.get_message(data, 'Para conhecer é só entrar no group: https://t.me/mise4s')
                            group = 0
                        
                        if 'new_chat_members' in data_message:
                                group = 1
                                novos_membros = data_message['new_chat_members']
                                for membro in novos_membros:
                                    nome_do_membro = membro['first_name']
                                    message.get_message(data, f'Seja muito bem-vindo {nome_do_membro}')
                                    message.get_message(data, """Aqui temos:
Verificação de quem manda video, fotos, links,
Entra no grupo,
controle de assinatura,
Programa conteudo,
Gerenciamento de quem sai, 
e muito mais
agora vamos remover do grupo em 30 segundos é so voltar no chat para falar com atendente.""")
                                    time.sleep(10)
                                    message.remover_membro_do_grupo(data)
                                    message.get_message_client(client, "você pode pedir mais informações ou fazer um orçamento se quiser, https://api.whatsapp.com/send?phone=5511971805330&text=Ol%C3%A1%20quero%20um%20or%C3%A7amento%20do%20Bot%20do%20telegram")
        



            except Exception as e:
                    print('error:', e)
                    logging.error(f"Erro ao processar atualizações para o bot {self.token}: {e}")