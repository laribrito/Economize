from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

#carrega a tela .kv correspondente
Builder.load_file("telas/adicionaRetirada.kv")

#Importa o banco de dados
from model import db

#Importa as configurações gerais do sistema
from appConfig import AppConfig

class AdicionaRetirada(Screen):
    #elementos da interface
    setMensagem = ObjectProperty(None)

    def adicionaRetirada(self, valor, descricao):
        valido = True
        
        #ERRO: 'valor' não é um número
        try:
            valor = float(valor)
        except ValueError:
            self.setMensagem.text = "Valor inválido. Digite somente números."
            valido = False

        #ERRO: valor de retirada é maior que o saldo da conta
        conta = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))
        try:
            if valor > conta[3]:
                self.setMensagem.text = "Valor inválido. Saldo insuficiente."
                valido=False
        except TypeError:
            pass

        #ERRO: algum campo vazio
        if valor == "" or descricao == "":
            self.setMensagem.text = "Preencha todos os campos."
            valido = False
        
        #SUCESSO
        if valido:
            #Banco de dados
            db.adiciona_retirada(valor,descricao, conta[0])
            
            #Volta para a página inicial
            self.manager.current = "principal"
            self.manager.transition.direction = "right"
            self.manager.current_screen.setMensagem.text = "Valor retirado com sucesso."
            self.manager.current_screen.atualizaSaldo()