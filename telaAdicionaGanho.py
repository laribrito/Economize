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
Builder.load_file("telas/adicionaGanho.kv")

#Importa o banco de dados
from model import db

#Importa as configurações gerais do sistema
from appConfig import AppConfig

class AdicionaGanho(Screen):

    #elementos da interface
    setMensagem = ObjectProperty(None)
    getValor = ObjectProperty(None)
    getDescricao = ObjectProperty(None)
    setSaldo = ObjectProperty(None)
    setConta = ObjectProperty(None)

    def atualizaSaldo(self, *args):
        dados = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))
        saldo = float(dados[3])
        self.setSaldo.text = f"R$ {saldo:.2f}"
        self.setConta.text = AppConfig.get_config("contaPadrao")

    def adicionaGanho(self, valor, descricao):
        valido = True
        
        #ERRO: 'valor' não é um número
        try:
            valor = float(valor)
        except ValueError:
            self.setMensagem.text = "Valor inválido. Digite somente números."
            valido = False
        
        #ERRO: algum campo vazio
        if valor == "" or descricao == "":
            self.setMensagem.text = "Preencha todos os campos."
            valido = False
            
        #SUCESSO
        if valido:
            #Busca o id da conta
            conta = db.retorna_conta_nome(AppConfig.get_config("contaPadrao"))

            #Banco de dados
            db.adiciona_ganho(valor,descricao, conta[0])
            
            #Limpa a tela do formulário
            self.getDescricao.text = ""
            self.getValor.text = ""

            #Volta para a página inicial
            self.manager.current = "principal"
            self.manager.transition.direction = "right"
            self.manager.current_screen.setMensagem.text = "Valor adicionado com sucesso."
            self.manager.current_screen.atualizaSaldo()
            self.manager.current_screen.mostrarMovimentacoes()