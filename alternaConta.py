from types import LambdaType
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

Builder.load_file("telas/alternaConta.kv")

#importa o banco de dados
from model import db

#importa as configurações gerais do sistema
from appConfig import AppConfig

class AlternaConta(Screen):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(AlternaConta, self).__init__(**kwargs)

        rolagem = ScrollView(pos_hint={"top": 0.9}, size_hint_y=0.8)
        
        layout = BoxLayout(size_hint_y=None)
        
        x = 0
        if x == 0:
            layout.add_widget(Label(text="Não há contas cadastradas ainda", size_hint_y=None))
        else:
            Contas = GridLayout(cols=2, size_hint_y=None)
            for i in range(x):
                Contas.add_widget(Label(text='Conta', size_hint_y=None))
                Contas.add_widget(Label(text='Saldo', size_hint_y=None))
                Contas.add_widget(Label(text='Tipo', size_hint_y=None))
                Contas.add_widget(Button(text='Tornar\npadrão', size_hint_y=None))

            layout.add_widget(Contas)
            layout.add_widget(Label(text="Fim", size_hint_y=None))

        rolagem.add_widget(layout)
        self.add_widget(rolagem, index=1)

        
    