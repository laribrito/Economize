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
from functools import partial
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty

#carrega a tela .kv correspondente
Builder.load_file("telas/adicionaGanho.kv")

#Importa o banco de dados
from model import db

#Importa as configurações gerais do sistema
from appConfig import AppConfig

#Essa classe foi criada para manter a tela inicial 
# organizada . Ela limita a entrada da descrição a 
# 35 caracteres
class LimitInputGanho(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_active= 'imgs/bordaBotaoAtivoVerde.png'

    def keyboard_on_key_up(self, keycode, text):
        if text[0] == 'backspace':
            self.do_backspace()

    def on_text(self, instance, value):
        if len(self.text) >= 36:
            self.text = self.text[:35]

#CLASS KV
class AdicionaGanho(Screen):
    #elementos da interface
    getValor = ObjectProperty(None)
    getDescricao = ObjectProperty(None)
    setSaldo = ObjectProperty(None)
    setConta = ObjectProperty(None)
    labelDesc = ObjectProperty(None)
    erroValor = ObjectProperty(None)
    erroDesc = ObjectProperty(None)

    #Contador para a máscara
    Count = NumericProperty(0)

    #Método para atualizar o label abaixo do campo descrição
    def atualizaNumDescricao(self, texto):
        tamanho = len(texto)
        self.labelDesc.text=f"{tamanho}/35"

    #Método para o valor que fica no canto superior esquerdo
    def atualizaSaldo(self, *args):
        dados = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))
        saldo = float(dados[3])
        self.setSaldo.text = f"R$ {saldo:.2f}"
        self.setConta.text = AppConfig.get_config("contaPadrao")

    #Método para máscara no campo de valor
    def adicionarMascara(self, centavos):
        #Incrementa contador
        self.Count+=1    

        if self.Count%2!=0:
            #Remove os caracteres especiais
            valor = centavos[3:]
            #Retira as casas decimais
            valor = valor.split(".")
            valor = f"{valor[0]}{valor[1]}"
            try:
                #Transforma em número inteiro
                valor = int(valor)
                #Seleciona a parte inteira
                inteiros = valor//100
                #Seleciona a parte decimal
                cent = valor/100
                cent=f"{cent:.2f}"
                #Pega os dois últimos caracteres da string
                cent=cent[-2::]
                #Seta o novo valor no campo
                self.getValor.text=f"R$ {inteiros}.{cent}"
                #Limpa a mensagem de erro
                self.erroValor.text=" "
            except ValueError:
                #ERRO: não foi digitado um número
                self.erroValor.text="Somente números nesse campo"
                Clock.schedule_once(partial(self.limpaMensagens, 0), AppConfig.tempoLimpar)
                #Remove a letra digitada
                correcao=centavos[:-1]
                self.getValor.text = correcao

    #Método para adicionar um ganho
    def adicionaGanho(self, valor, descricao):
        valido = True
        
        #ERRO: 'valor' não é um número
        try:
            #Retira a string da máscara
            valor = valor[3:]
            #Tenta transformar a string em número
            valor = float(valor)
        except ValueError:
            self.erroValor.text="Somente números nesse campo"
            valido = False
            Clock.schedule_once(partial(self.limpaMensagens, 0), AppConfig.tempoLimpar)
        
        #ERRO: algum campo vazio
        if valor == 0 or descricao == "":
            if valor == 0:
                self.erroValor.text="Preencha antes de continuar"
                Clock.schedule_once(partial(self.limpaMensagens, 0), AppConfig.tempoLimpar)
            if descricao=="":
                self.erroDesc.text="Preencha antes de continuar"
                Clock.schedule_once(partial(self.limpaMensagens, 1), AppConfig.tempoLimpar)
            valido = False
            
        #SUCESSO
        if valido:
            #Busca o id da conta
            conta = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))

            #Banco de dados
            db.adiciona_ganho(valor,descricao, conta[0])
            
            #Limpa a tela do formulário
            self.getDescricao.text = ""
            self.getValor.text = "R$ 0.00"

            #Volta para a página inicial
            self.manager.current = "principal"
            self.manager.transition.direction = "right"
            self.manager.current_screen.criarMensagem("Valor adicionado com sucesso")
            self.manager.current_screen.atualizaSaldo()
            self.manager.current_screen.mostrarMovimentacoes()
    
      #Esse é um evento disparado quando sai dessa tela
    
    def limpaMensagens(self, tipo, dt):
        if tipo==0:
            self.erroValor.text = " "
        else:
            self.erroDesc.text = " "

    #Esse é um evento disparado quando sai dessa tela
    def on_leave(self, *args):
        #Limpa o formulário
        self.getValor.text="R$ 0.00"
        self.getDescricao.text=""
        Clock.unschedule(self.eventoCursorValor)
        return super().on_leave(*args)
    
    def on_enter(self, *args):
        self.getValor.focus=True
        #POR UM bug QUE APARECEU 
        #Joga o cursor para o final do textInput
        #  contra o que o do_backspace faz
        Clock.schedule_interval(self.eventoCursorValor, 0.01)
        return super().on_enter(*args)

    def eventoCursorValor(self, *args):
        self.getValor.do_cursor_movement('cursor_end')
    
    #Esse trio de funções serve para a utilização correta
    # da tecla "esc" e do botão voltar do android
    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)
        return super().on_pre_enter(*args)

    def voltar(self, window, key, *args):
        if key == 27:
            self.manager.current="principal"
            self.manager.transition.direction="right"
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)
        return super().on_pre_leave(*args)
        