from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from functools import partial
from kivy.properties import ObjectProperty

#Carrega a tela .kv correspondente
Builder.load_file("telas/alternaConta.kv")

#Importa o banco de dados
from model import db

#Importa as configurações gerais do sistema
from appConfig import AppConfig

class AlternaConta(Screen):
    #Listas que armazenarão objetos da tela
    raiz = []
    box = []

    #Torna a conta selecionada como a padrão, que será exibida na tela principal
    def tornaPadrao(self, *args):
        AppConfig.set_config("contaPadrao", args[1])
        self.manager.current="principal"
        self.manager.transition.direction = "right"
        self.manager.current_screen.setMensagem.text = 'Conta padrão alterada com sucesso!'
        self.manager.current_screen.atualizaSaldo()

    def exibirContas(self):
        #ScrollView
        rolagem = ScrollView(pos_hint={"top": 0.9}, size_hint_y=0.8)

        #BoxLayout
        #Ele é necessário por causa da mensagem final e 
        # da mensagem para nenhuma conta cadastrada
        layout = BoxLayout(size_hint_y=None)

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
        
        #Busca as contas cadastradas no banco de dados
        contas = db.retorna_contas()
        #Lê quantas são
        quant = len(contas)

        if quant == 0:
            layout.add_widget(Label(text="Não há contas cadastradas ainda", size_hint_y=None))
        else:
            #Adiciona os widgets à tela
            #GridLayout
            Contas = GridLayout(cols=2, size_hint_y=None)
            for ind, conta in enumerate(contas):
                #Nome da conta
                Contas.add_widget(Label(text=conta[1], size_hint_y=None))
                
                #Saldo da conta
                Contas.add_widget(Label(text=f"R$ {conta[3]:.2f}", size_hint_y=None))

                #Tipo da conta
                Contas.add_widget(Label(text=f"{conta[2]}", size_hint_y=None))

                #Botão para tornar essa conta a conta padrão
                btn = Button(text='Tornar\npadrão', size_hint_y=None)
                #Ligação do botão com a função 'tornaPadrão()'
                btn.bind(on_press=partial(self.tornaPadrao, ind, conta[1]))
                Contas.add_widget(btn)

            #Adiciona o GridLayout que contem as contas
            layout.add_widget(Contas)
            layout.add_widget(Label(text="Fim", size_hint_y=None))

        #Salva o objeto Boxlayout
        self.box = layout
        rolagem.add_widget(layout)
        #Salva o objeto ScrollView
        self.raiz = rolagem
        self.add_widget(rolagem)

        
    