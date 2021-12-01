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
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.clock import Clock

#carrega a tela .kv correspondente
Builder.load_file("telas/adicionaConta.kv")

#importa o banco de dados
from model import db

#importa as configurações gerais do sistema
from appConfig import AppConfig

class BtnPrincipal(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height= self.texture_size[1] + dp(40)
        self.markup=True
        self.background_normal="telas/imgs/bordaBotao.png"
        self.background_down="telas/imgs/bordaBotao.png"
        self.color="#272727"

class BtnDropDown(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal="telas/imgs/borda.png"
        self.background_color="#FFFFFF"
        self.color="#000000"

class AdicionaConta(Screen):

    #elementos da interface
    setMensagem = ObjectProperty(None)
    getNome = ObjectProperty(None)
    getPadrao = ObjectProperty(None)
    # getTipo = ObjectProperty(None)
    layoutTipo = ObjectProperty(None)

    #Tipos de conta que o programa trabalha
    tiposDisponiveis=["Dinheiro", "Saldo"   , "Investimento"]

    #Tipo selecionado
    tipoEscolhido = ""

    def __init__(self, **kw):
        super().__init__(**kw)
        #Menu dropdown
        
        #Botão principal
        btn_principal = BtnPrincipal(text="Escolha o tipo")
        self.layoutTipo.add_widget(btn_principal)
        
        #Itens dropdown
        dropdown = DropDown()
        for index in range(len(self.tiposDisponiveis)):
            btn = BtnDropDown(text = f'[color=#ffffff00]{index+1}[/color]{self.tiposDisponiveis[index]} ', size_hint_y = None, height = 44, 
            on_release = lambda btn: self.escolheuTipo(btn),
            markup=True)

            # binding the button to show the text when selected
            btn.bind(on_release = lambda btn: dropdown.select(btn.text))

            # then add the button inside the dropdown
            dropdown.add_widget(btn)
        
        btn_principal.bind(on_release = dropdown.open)

        # one last thing, listen for the selection in the
        # dropdown list and assign the data to the button text.
        dropdown.bind(on_select = lambda instance, x: setattr(btn_principal, 'text', x))

    def escolheuTipo(self, instance):
        self.tipoEscolhido=instance.text[17]
        
    def cadastraConta(self, nome, padrao):
        valido = True

        #ERRO: já existe uma conta com o nome informado
        conta = db.retorna_conta_nome(nome)
        if conta != None:
            self.setMensagem.text = "Essa conta já existe. Insira um outro nome."
            valido = False

        #ERRO: 'tipo' não é um número
        try:
            tipo = int(self.tipoEscolhido)
            #ERRO: valor de 'tipo' não é um valor disponível
            if tipo > len(self.tiposDisponiveis) or tipo < 1:
                self.setMensagem.text = "Tipo de conta inválido. Valor não disponível."
                valido = False
        except ValueError:
            self.setMensagem.text = "Tipo de conta inválido. Digite um número."
            valido = False
        
        #ERRO: algum campo vazio
        if nome == "" or self.tipoEscolhido =="":
            
            self.setMensagem.text = "Preencha todos os campos."
            valido = False

        #SUCESSO
        if valido:
            db.cria_conta(nome,tipo)
            novaConta = db.retorna_conta_nome(nome)
            if padrao:
                #guarda a conta que foi criada como conta padrão
                AppConfig.set_config("contaPadrao", nome)
                AppConfig.set_config("idConta", novaConta[0])

            self.getNome.text = ""
            # self.getTipo.text = ""
            self.getPadrao.active = False

            #muda para a tela inicial
            self.manager.current="principal"
            self.manager.transition.direction = "right"
            self.manager.current_screen.setMensagem.text = 'Conta adicionada com sucesso!'
            self.manager.current_screen.atualizaSaldo()
            self.manager.current_screen.mostrarMovimentacoes()
            
