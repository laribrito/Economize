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
from functools import partial
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.metrics import dp

#carrega a tela .kv correspondente
Builder.load_file("telas/adicionaConta.kv")

#importa o banco de dados
from model import db

#importa as configurações gerais do sistema
from appConfig import AppConfig

#CLASSE KV
class AdicionaConta(Screen):

    #elementos da interface
    getNome = ObjectProperty(None)
    getPadrao = ObjectProperty(None)
    erroNome = ObjectProperty(None)
    erroTipo = ObjectProperty(None)
    tipoI = ObjectProperty(None)
    tipoII = ObjectProperty(None)
    tipoIII = ObjectProperty(None)
    #Conjunto de botões dos tipo de conta
    # que será montado no on_enter()
    # para poder limpa-los no on_leave()
    tiposInterface = []

    #Tipos de conta que o programa trabalha
    tiposDisponiveis= AppConfig.tipos

    #Tipo selecionado
    tipoEscolhido = ""
    
    #Método para mudar o tipo escolhido
    def escolheuTipo(self, *tipos):
        escolheu = False
        #Percorre a lista de botões
        for i in tipos:
            if i.state == "down":
                #Se algum botão estiver selecionado, a cor da sua letra é alterada 
                # para branco, o valor é armazenado na classe e 'escolheu' sinaliza
                # que o usuário escolheu algum valor
                i.color=(1,1,1,1)
                escolheu = True
                self.tipoEscolhido=i.valor
            else:
                #Todo botão que não estiver selecionado deve manter a fonte preta
                i.color=(0,0,0,1)
        #Se não houver botão selecionado, então um valor vazio deve ser sobrescrito
        if not escolheu:
            self.tipoEscolhido=""
    
    #Método para cadastrar uma conta
    def cadastraConta(self, nome, padrao):
        valido = True

        #ERRO: já existe uma conta com o nome informado
        conta = db.retorna_conta_nome(nome)
        if conta != None:
            self.erroNome.text = "Essa conta já existe. Insira um outro nome"
            valido = False
            Clock.schedule_once(partial(self.limpaMensagens,0), AppConfig.tempoLimpar)

        #ERRO: 'tipo' não é um número
        try:
            tipo = int(self.tipoEscolhido)
            #ERRO: valor de 'tipo' não é um valor disponível
            if tipo > len(self.tiposDisponiveis) or tipo < 1:
                self.erroTipo.text = "Tipo de conta inválido. Valor não disponível"
                valido = False
                Clock.schedule_once(partial(self.limpaMensagens,1), AppConfig.tempoLimpar)
                
        except ValueError:
            self.erroTipo.text = "Tipo de conta inválido. Digite um número"
            valido = False
            Clock.schedule_once(partial(self.limpaMensagens,1), AppConfig.tempoLimpar)
        
        #ERRO: algum campo vazio
        if nome == "" or self.tipoEscolhido =="":
            valido = False
            if nome == "":
                self.erroNome.text="Preencha antes de continuar"
                Clock.schedule_once(partial(self.limpaMensagens, 0), AppConfig.tempoLimpar)
            if self.tipoEscolhido=="":
                self.erroTipo.text="Preencha antes de continuar"
                Clock.schedule_once(partial(self.limpaMensagens, 1), AppConfig.tempoLimpar)

        #SUCESSO
        if valido:
            db.cria_conta(nome,tipo)
            novaConta = db.retorna_conta_nome(nome)
            if padrao:
                #guarda a conta que foi criada como conta padrão
                AppConfig.set_config("contaPadrao", nome)
                AppConfig.set_config("idConta", novaConta[0])

            #muda para a tela inicial
            self.manager.current="principal"
            self.manager.transition.direction = "right"
            self.manager.current_screen.criarMensagem('Conta adicionada com sucesso')
            self.manager.current_screen.atualizaSaldo()
            self.manager.current_screen.mostrarMovimentacoes()
    
    #Método para trocar o estado do checkbox pelo toque
    # no label
    def trocaCheck(self, *args):
        antigoValor = self.getPadrao.active
        novoValor = not antigoValor 
        self.getPadrao.active = novoValor

    #Método para limpar as mensagens inline do form
    # cada tipo corresponde a um campo
    def limpaMensagens(self, tipo, dt):
        if tipo==0:
            self.erroNome.text = " "
        else:
            self.erroTipo.text = " "

    #Esse é um evento disparado quando sai dessa tela
    def on_leave(self, *args):
        #Limpa o formulário
        self.getNome.text=""
        self.tipoEscolhido=""
        self.getPadrao.active=False
        tipos = self.tiposInterface
        for i in tipos:
            i.state="normal"
            i.color=(0,0,0,1)
        self.tiposInterface.clear()
        return super().on_leave(*args)
    
    #Esse é um evento disparado quando o app entra nessa tela
    def on_enter(self, *args):
        self.getNome.focus=True
        #Monta a lista com os botões de tipo
        self.tiposInterface.append(self.tipoI)
        self.tiposInterface.append(self.tipoII)
        self.tiposInterface.append(self.tipoIII)
        return super().on_enter(*args)
    
    #Esse trio de funções serve para a utilização correta
    # da tecla "esc" e do botão voltar do android
    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.voltar)
        return super().on_pre_enter(*args)

    def voltar(self, window, key, *args):
        if key == 27:
            self.manager.current="alteraContas"
            self.manager.transition.direction="right"
            return True

    def on_pre_leave(self, *args):
        Window.unbind(on_keyboard=self.voltar)
        return super().on_pre_leave(*args)