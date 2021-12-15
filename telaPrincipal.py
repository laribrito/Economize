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

#carrega a tela .kv correspondente
Builder.load_file("telas/principal.kv")

#importa o banco de dados
from model import db

#importa as configurações gerais do sistema
from appConfig import AppConfig

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
        time.sleep(0.1)
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
            time.sleep(0.1)
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
                time.sleep(0.1)
                self.mostrarBotoes()
                
        else:
            #ERRO: Não tem uma conta como padrão para receber a transação
            self.setMensagem.text = "Para adicionar uma retirada é\nnecessário uma conta padrão."
    
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
        
        for i in tudo:
            print(i)

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
                        color=(0,.9,0,1)
                    )
                    valor = Label(
                        text=f" R${movimentacao[1]:.2f} "
                    )
                    desc = Label(
                        text=f" {movimentacao[2]} "
                    )
                    grid.add_widget(sinal)
                    grid.add_widget(valor)
                    grid.add_widget(desc)
                else:
                    sinal = Label(
                        text=" - ",
                        color=(.9,0,0,1)
                    )
                    valor = Label(
                        text=f" R${movimentacao[1]:.2f} "
                    )
                    desc = Label(
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