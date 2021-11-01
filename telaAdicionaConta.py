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

#carrega a tela .kv correspondente
Builder.load_file("telas/adicionaConta.kv")

#importa o banco de dados
from model import db

#importa as configurações gerais do sistema
from appConfig import AppConfig

class AdicionaConta(Screen):

    #elementos da interface
    setMensagem = ObjectProperty(None)
    getNome = ObjectProperty(None)
    getPadrao = ObjectProperty(None)
    getTipo = ObjectProperty(None)

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
            novaConta = db.retorna_conta_nome(nome)
            if padrao:
                #guarda a conta que foi criada como conta padrão
                AppConfig.set_config("contaPadrao", nome)
                AppConfig.set_config("idConta", novaConta[0])

            self.getNome.text = ""
            self.getTipo.text = ""
            self.getPadrao.active = False

            #muda para a tela inicial
            self.manager.current="principal"
            self.manager.transition.direction = "right"
            self.manager.current_screen.setMensagem.text = 'Conta adicionada com sucesso!'
            self.manager.current_screen.atualizaSaldo()
            self.manager.current_screen.mostrarMovimentacoes()
            
