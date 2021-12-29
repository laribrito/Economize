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
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty

#carrega a tela .kv correspondente
Builder.load_file("telas/adicionaRetirada.kv")

#Importa o banco de dados
from model import db

#Importa as configurações gerais do sistema
from appConfig import AppConfig

#Essa classe foi criada para manter a tela inicial 
# organizada . Ela limita a entrada da descrição a 
# 35 caracteres
class LimitInputRetirada(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_active= 'imgs/bordaBotaoAtivoVermelho.png'

    def keyboard_on_key_up(self, keycode, text):
        if text[0] == 'backspace':
            self.do_backspace()

    def on_text(self, instance, value):
        if len(self.text) >= 36:
            self.text = self.text[:35]

#CLASS KV
class AdicionaRetirada(Screen):
    
    #elementos da interface
    setMensagem = ObjectProperty(None)
    getValor = ObjectProperty(None)
    getDescricao = ObjectProperty(None)
    setSaldo = ObjectProperty(None)
    setConta = ObjectProperty(None)

    #Método para o valor que fica no canto superior esquerdo
    def atualizaSaldo(self, *args):
        dados = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))
        saldo = float(dados[3])
        self.setSaldo.text = f"R$ {saldo:.2f}"
        self.setConta.text = AppConfig.get_config("contaPadrao")

    #Método para adicionar uma retirada
    def adicionaRetirada(self, valor, descricao):
        valido = True
        
        #ERRO: 'valor' não é um número
        try:
            valor = float(valor)
        except ValueError:
            self.setMensagem.text = "Valor inválido. Digite somente números."
            valido = False
            Clock.schedule_once(self.limpaMensagens, AppConfig.tempoLimpar)

        #ERRO: valor de retirada é maior que o saldo da conta
        conta = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))
        try:
            if valor > conta[3]:
                self.setMensagem.text = "Valor inválido. Saldo insuficiente."
                valido=False
                Clock.schedule_once(self.limpaMensagens, AppConfig.tempoLimpar)

        except TypeError:
            pass

        #ERRO: algum campo vazio
        if valor == "" or descricao == "":
            self.setMensagem.text = "Preencha todos os campos."
            valido = False
            Clock.schedule_once(self.limpaMensagens, AppConfig.tempoLimpar)
        
        #SUCESSO
        if valido:
            #Banco de dados
            db.adiciona_retirada(valor,descricao, conta[0])
            
            #Limpa a tela do formulário
            self.getDescricao.text = ""
            self.getValor.text = ""

            #Volta para a página inicial
            self.manager.current = "principal"
            self.manager.transition.direction = "right"
            self.manager.current_screen.setMensagem.text = "Valor retirado com sucesso."
            Clock.schedule_once(self.manager.current_screen.limpaMensagens, AppConfig.tempoLimpar)
            self.manager.current_screen.atualizaSaldo()
            self.manager.current_screen.mostrarMovimentacoes()
    
    def limpaMensagens(self, dt):
        self.setMensagem.text = ""


    #Esse é um evento disparado quando sai dessa tela
    def on_leave(self, *args):
        #Limpa o formulário
        self.getValor.text=""
        self.getDescricao.text=""
        return super().on_leave(*args)

    def on_enter(self, *args):
        self.getValor.focus=True
        return super().on_enter(*args)
