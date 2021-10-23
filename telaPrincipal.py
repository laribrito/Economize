from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty

#carrega a tela .kv correspondente
Builder.load_file("telas/principal.kv")

#importa o banco de dados
from model import db

#importa as configurações gerais do sistema
from appConfig import AppConfig

class Principal(Screen):
    setSaldo = ObjectProperty(None)
    setConta = ObjectProperty(None)
    setMensagem = ObjectProperty(None)
    def atualizaSaldo(self):
        if AppConfig.get_config("contaPadrao") != "":
            dados = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))
            saldo = float(dados[3])
            self.setSaldo.text = f"R$ {saldo:.2f}"
            self.setConta.text = AppConfig.get_config("contaPadrao")
        else:
            self.setSaldo.text = "Olá!"
            self.setConta.text = ""

    def podeAdicionarGanho(self):
        if AppConfig.get_config("contaPadrao") != "":
            self.manager.current="adicionaGanho"
            self.manager.transition.direction="left"
            #left para entrar na página
            #right para sair
        else:
            #ERRO: Não tem uma conta como padrão para receber a transação
            self.setMensagem.text = "Para adicionar um ganho é\nnecessário uma conta padrão."
    
    def podeAdicionarRetirada(self):
        if AppConfig.get_config("contaPadrao") != "":
            conta = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))
            if conta[3] == 0:
                #ERRO: Saldo da conta padrão é igual a 0
                self.setMensagem.text = "Para adicionar um ganho é\nnecessário saldo maior que zero."
            else:
                self.manager.current="adicionaRetirada"
                self.manager.transition.direction="left"
                #left para entrar na página
                #right para sair
        else:
            #ERRO: Não tem uma conta como padrão para receber a transação
            self.setMensagem.text = "Para adicionar um ganho é\nnecessário uma conta padrão."