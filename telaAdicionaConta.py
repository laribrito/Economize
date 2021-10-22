from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

#carrega a tela .kv correspondente
Builder.load_file("telas/adicionaConta.kv")

#importa o banco de dados
from model import db

#importa as configurações gerais do sistema
from appConfig import AppConfig

class AdicionaConta(Screen):

    #elementos da interface
    setMensagem = ObjectProperty(None)

    def cadastraConta(self, nome, tipo, padrao):
        valido = True

        #ERRO: já existe uma conta com o nome informado
        conta = db.retorna_conta_nome(nome)
        if conta != None:
            self.setMensagem.text = "Essa conta já existe. Insira um outro nome."
            valido = False

        #ERRO: 'tipo' não é um número
        try:
            tipo = int(tipo)
            #ERRO: valor de 'tipo' não é um valor disponível
            if tipo > 3 or tipo < 1:
                self.setMensagem.text = "Tipo de conta inválido. Valor não disponível."
                valido = False
        except ValueError:
            self.setMensagem.text = "Tipo de conta inválido. Digite um número."
            valido = False
        
        #ERRO: algum campo vazio
        if nome == "" or tipo =="":
            
            self.setMensagem.text = "Preencha todos os campos."
            valido = False

        #SUCESSO
        if valido:
            db.cria_conta(nome,tipo)
            if padrao:
                #guarda a conta que foi criada como conta padrão
                AppConfig.set_config("contaPadrao", nome)
            #muda para a tela inicial
            self.manager.current="principal"
            self.manager.transition.direction = "right"
            self.manager.current_screen.setMensagem.text = 'Conta adicionada com sucesso!'
            self.manager.current_screen.atualizaSaldo()
            
