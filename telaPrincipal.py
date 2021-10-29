from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from functools import partial

#carrega a tela .kv correspondente
Builder.load_file("telas/principal.kv")

#importa o banco de dados
from model import db

#importa as configurações gerais do sistema
from appConfig import AppConfig

class Principal(Screen):

    #Elementos da interface
    setSaldo = ObjectProperty(None)
    setConta = ObjectProperty(None)
    setMensagem = ObjectProperty(None)
    boxBotoes = ObjectProperty(None)

    estadoBotao = False

    def mostrarBotoes(self):
        if self.estadoBotao:
            #Se o estado for True, limpa a tela
            self.boxBotoes.clear_widgets()

            #Troca a tela do botão
            self.estadoBotao = not self.estadoBotao
        else:
            #Se o estado for False, exibe os botoes

            #ADICIONA GANHO
            btn1 = Button(
            size_hint=(None,None),
            pos_hint={"x": 0.8, "y": 0.5},
            size=('60','60'),
            border=(0,0,0,0),
            background_normal="telas/imgs/mais_normal.png",
            background_down="telas/imgs/mais_down.png"
            )
            btn1.bind(on_press=self.podeAdicionarGanho)
            self.boxBotoes.add_widget(btn1)                        

            #CONTAS
            btn3 = Button(
            pos_hint={"x": 0.64, "y": 0.35},
            size_hint=(None,None),
            size=('60','60'),
            border=(0,0,0,0),
            background_normal="telas/imgs/contas_normal.png",
            background_down="telas/imgs/contas_down.png"
            )
            btn3.bind(on_press=self.telaContas)
            self.boxBotoes.add_widget(btn3)

            #ADICIONA RETIRADA
            btn2 = Button(
            pos_hint= {"x": 0.55, "y": 0.07},
            size_hint=(None,None),
            size=('60','60'),
            border=(0,0,0,0),
            background_normal="telas/imgs/menos_normal.png",
            background_down="telas/imgs/menos_down.png"
            )
            btn2.bind(on_press=self.podeAdicionarRetirada)
            self.boxBotoes.add_widget(btn2)

            #Troca o estado do botão
            self.estadoBotao = not self.estadoBotao

    def telaContas(self,*args):
        #Muda de tela
        self.manager.current="alteraContas"
        self.manager.transition.direction="left"
        self.manager.current_screen.exibirContas()

        #Fecha o menu da tela principal
        # como ele já trocou o 'estadoBotao',
        # só basta recarregar o método
        self.mostrarBotoes()
        

    def atualizaSaldo(self, *args):
        if AppConfig.get_config("contaPadrao") != "":
            dados = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))
            saldo = float(dados[3])
            self.setSaldo.text = f"R$ {saldo:.2f}"
            self.setConta.text = AppConfig.get_config("contaPadrao")
        else:
            self.setSaldo.text = "Olá!"
            self.setConta.text = ""

    def podeAdicionarGanho(self, *args):
        if AppConfig.get_config("contaPadrao") != "":
            #Muda de tela
            self.manager.current="adicionaGanho"
            self.manager.transition.direction="left"
            self.manager.current_screen.atualizaSaldo()

            #Fecha o menu da tela principal
            # como ele já trocou o 'estadoBotao',
            # só basta recarregar o método
            self.mostrarBotoes()        
        else:
            #ERRO: Não tem uma conta como padrão para receber a transação
            self.setMensagem.text = "Para adicionar um ganho é\nnecessário uma conta padrão."
    
    def podeAdicionarRetirada(self, *args):
        if AppConfig.get_config("contaPadrao") != "":
            conta = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))
            if conta[3] == 0:
                #ERRO: Saldo da conta padrão é igual a 0
                self.setMensagem.text = "Para adicionar uma retirada é\nnecessário saldo maior que zero."
            else:
                #Muda de tela
                self.manager.current="adicionaRetirada"
                self.manager.transition.direction="left"
                self.manager.current_screen.atualizaSaldo()

                #Fecha o menu da tela principal
                # como ele já trocou o 'estadoBotao',
                # só basta recarregar o método
                self.mostrarBotoes()
                
        else:
            #ERRO: Não tem uma conta como padrão para receber a transação
            self.setMensagem.text = "Para adicionar uma retirada é\nnecessário uma conta padrão."