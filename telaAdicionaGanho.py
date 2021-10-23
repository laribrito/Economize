from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

#carrega a tela .kv correspondente
Builder.load_file("telas/adicionaGanho.kv")

#Importa o banco de dados
from model import db

#Importa as configurações gerais do sistema
from appConfig import AppConfig

class AdicionaGanho(Screen):

    #elementos da interface
    setMensagem = ObjectProperty(None)

    def adicionaGanho(self, valor, descricao):
        valido = True
        
        #ERRO: 'valor' não é um número
        try:
            valor = float(valor)
        except ValueError:
            self.setMensagem.text = "Valor inválido. Digite somente números."
            valido = False
        
        #ERRO: algum campo vazio
        if valor == "" or descricao == "":
            self.setMensagem.text = "Preencha todos os campos."
            valido = False
            
        #SUCESSO
        if valido:
            #Busca o id da conta
            conta = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))

            #Banco de dados
            db.adiciona_ganho(valor,descricao, conta[0])
            
            #Volta para a página inicial
            self.manager.current = "principal"
            self.manager.transition.direction = "right"
            self.manager.current_screen.setMensagem.text = "Valor adicionado com sucesso."
            self.manager.current_screen.atualizaSaldo()