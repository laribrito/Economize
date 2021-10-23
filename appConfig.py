'''
Classe AppConfig.

Esta classe será responsável por manipular algumas configurações da aplicação.
Estas configurações serão salvas no arquivo config.json no mesmo diretório da aplicação.

Altere o atributo 'servidor' desta classe para indicar o endereço do web service.

obs.: Basicamente eu copiei esse arquivo do repositório do meu prof e vou estudar a lógica 
por trás desse arquivo. Obrigada JP!
'''

import json

class AppConfig:
    config = {}

    '''
    Carrega a configuração do arquivo JSON.

    Se o arquivo não existir, a configuração permanecerá vazia.
    '''
    def carrega_config():
        try:
            arq = open('config.json', 'r')
            AppConfig.config = json.load(arq)
            arq.close()

        except FileNotFoundError:
            AppConfig.config = {}
    
    '''
    Salva a configuração atual no arquivo JSON.
    '''
    def salva_config():
        arq = open('config.json', 'w')
        json.dump(AppConfig.config, arq)
        arq.close()

    '''
    Retorna um valor da configuração.

    O valor é buscado pela chave do dicionário. Se a chave não
    existir no dicionário, retorna None.
    '''
    def get_config(chave):
        # Antes verifica se o arquivo já foi carregado
        if (AppConfig.config == {}):
            AppConfig.carrega_config()

        # Retorna o valor da chave. Se a chave não existir, retorna None.
        try:
            return AppConfig.config[chave]
        except KeyError:
            return ""
    
    '''
    Altera um item de configuração.

    Ao receber o par chave/valor, o valor da chave é atualizado na configuração
    (caso a chave não exista, será criada) e o dicionário é automaticamente
    salvo no arquivo JSON.
    '''
    def set_config(chave, valor):
        AppConfig.config[chave] = valor
        AppConfig.salva_config()