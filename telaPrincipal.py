"""
This file is part of Economize!.

Economize! is free software: you can redistribute
it and/or modify it under the terms of the GNU General Public License 
as published by the Free Software Foundation, either version 3 of
the License, or any later version.

Economize! is distributed in the hope that 
it will be useful, but WITHOUT ANY WARRANTY; without even the 
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Economize!.  If not, see <https://www.gnu.org/licenses/>.
"""

from kivy.core import window
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
import time
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

#carrega a tela .kv correspondente
Builder.load_file("telas/principal.kv")

#importa o banco de dados
from model import db

#importa as configurações gerais do sistema
from appConfig import AppConfig

#Classe para a descrição do ganho/retirada
class Desc(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_size=(Window.width*2)/4, None
        # self.max_lines = 2
    #     with self.canvas.before:
    #         Color(0.1,0.4,1,1)
    #         self.rect = Rectangle(pos=self.pos, size=self.size)

    #     self.bind(pos=self.update_rect)
    #     self.bind(size=self.update_rect)

    # def update_rect(self, *args):
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size

#Classe para os botões da tela inicial
class BtnImagensPrincipal(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size=(f'{Window.width*0.14}',f'{Window.width*0.14}')
        self.border=(0,0,0,0)
        self.size_hint=(None,None)

#CLASSE KV
class Principal(Screen):
    #Listas que armazenarão objetos da tela
    raiz = []
    box = []

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

        else:
            #Se o estado for False, exibe os botoes

            #ADICIONA GANHO
            btn1 = BtnImagensPrincipal(
            y=Window.width - ((Window.width*3)/5) - (Window.width*0.14),
            x=Window.width - (Window.width/40) - (Window.width*0.14),
            background_normal="telas/imgs/mais_normal.png",
            background_down="telas/imgs/mais_down.png"
            )
            btn1.bind(on_press=self.podeAdicionarGanho)
            self.boxBotoes.add_widget(btn1)                        

            #CONTAS
            btn3 = BtnImagensPrincipal(
            y=Window.width/5,
            x=Window.width - (Window.width/5) - (Window.width*0.14),
            background_normal="telas/imgs/contas_normal.png",
            background_down="telas/imgs/contas_down.png"
            )
            btn3.bind(on_press=self.telaContas)
            self.boxBotoes.add_widget(btn3)

            # print(Window.width)

            #ADICIONA RETIRADA
            btn2 = BtnImagensPrincipal(
            y=Window.width/40,
            x=(Window.width*3)/5,
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

        #O método que estava aqui será chamado pelo evento on_leave() 

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

            #O método que estava aqui será chamado pelo evento on_leave()        
        else:
            #ERRO: Não tem uma conta como padrão para receber a transação
            self.setMensagem.text = "Para adicionar um ganho é\nnecessário uma conta padrão."
            Clock.schedule_once(self.limpaMensagens, AppConfig.tempoLimpar)
    
    def podeAdicionarRetirada(self, *args):
        if AppConfig.get_config("contaPadrao") != "":
            conta = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))
            if conta[3] == 0:
                #ERRO: Saldo da conta padrão é igual a 0
                self.setMensagem.text = "Para adicionar uma retirada é\nnecessário saldo maior que zero."
                Clock.schedule_once(self.limpaMensagens, AppConfig.tempoLimpar)
            else:
                #Muda de tela
                self.manager.current="adicionaRetirada"
                self.manager.transition.direction="left"
                self.manager.current_screen.atualizaSaldo()

                #O método que estava aqui será chamado pelo evento on_leave()               
        else:
            #ERRO: Não tem uma conta como padrão para receber a transação
            self.setMensagem.text = "Para adicionar uma retirada é\nnecessário uma conta padrão."
            Clock.schedule_once(self.limpaMensagens, AppConfig.tempoLimpar)
    
    def mostrarMovimentacoes(self):
        #Para que a tela apareça de forma correta é necessário 
        # limpar a tela antes de carrega-la de novo
        try:
            #Limpa o ScrollView
            self.raiz.clear_widgets()
        except AttributeError:
            #Se não conseguir é porque 
            # é a primeira vez que a tela é aberta,
            # portanto não precisa de limpeza
            pass

        try:
            #limpa o BoxLayout
            self.box.clear_widgets()
        except AttributeError:
            #Se não conseguir é porque 
            # é a primeira vez que a tela é aberta,
            # portanto não precisa de limpeza
            pass

        #ScrollView
        rolagem = ScrollView(pos_hint={"top": 0.68}, size_hint_y=0.65)

        #BoxLayout
        layout = BoxLayout(size_hint_y=None, padding=(20,0), spacing=20)

        #Pega os dados
        ganhos = db.retorna_ganhos_id(AppConfig.get_config("idConta"))
        retiradas = db.retorna_retiradas_id(AppConfig.get_config("idConta"))
        

        #Marca cada um com seu respectivo tipo (se ganho, ou se retirada)
        G=[] #lista auxiliar
        for i in ganhos:
            i = list(i)
            i.append("g")
            G.append(i)

        R=[] #lista auxiliar
        for i in retiradas:
            i = list(i)
            i.append("r")
            R.append(i)

        #Junta em uma lista só
        tudo = G + R

        #Ordena pela datahora, do mais recente para o mais antigo
        tudo.sort(key=lambda x: x[4], reverse=True)

        if len(tudo) == 0:
            layout.add_widget(Label(text="Não há movimentações", 
                                    size_hint_y=None, 
                                    font_size="14sp", 
                                    height=dp(20),
                                    color=(.6,.6,.6,1)))
            #Salva o objeto Boxlayout
            self.box = layout
            rolagem.add_widget(layout)
            #Salva o objeto ScrollView
            self.raiz = rolagem
            self.add_widget(rolagem, index=2)
        else:
            grid = GridLayout(cols=3, size_hint_y=None)
            for movimentacao in tudo:
                if movimentacao[5] =="g":
                    sinal = Label(
                        text=" + ",
                        size_hint_x=0.05,
                        color=(0,.9,0,1)
                    )
                    valor = Label(
                        text=f" R${movimentacao[1]:.2f} ",
                        size_hint_x=0.4
                    )
                    desc = Desc(
                        text=f" {movimentacao[2]} "
                    )
                    grid.add_widget(sinal)
                    grid.add_widget(valor)
                    grid.add_widget(desc)
                else:
                    sinal = Label(
                        text=" - ",
                        size_hint_x=0.1,
                        color=(.9,0,0,1)
                    )
                    valor = Label(
                        text=f" R${movimentacao[1]:.2f} ",
                        size_hint_x=0.4
                    )
                    desc = Desc(
                        text=f" {movimentacao[2]} "
                    )
                    grid.add_widget(sinal)
                    grid.add_widget(valor)
                    grid.add_widget(desc)
                    
            #Adiciona o texto ao BOXLAYOUT
            layout.add_widget(grid)

            #Marca o fim da lista
            layout.add_widget(Label(text="Fim", 
                                    size_hint_y=None, 
                                    font_size="14sp", 
                                    height=dp(20),
                                    color=(.6,.6,.6,1)))

            #Salva o objeto Boxlayout
            self.box = layout
            rolagem.add_widget(layout)
            #Salva o objeto ScrollView
            self.raiz = rolagem
            self.add_widget(rolagem, index=2)

    def limpaMensagens(self, dt):
        self.setMensagem.text = ""

    def on_leave(self, *args):
        #Fecha o menu da tela principal
        # como ele já trocou o 'estadoBotao',
        # só basta recarregar o método
        self.mostrarBotoes()  

        #Limpa as mensagens de erro
        self.setMensagem.text = ""
        return super().on_leave(*args)
        