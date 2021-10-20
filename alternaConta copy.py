from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
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

        setContas = ObjectProperty(None)
        
        Contas = GridLayout(cols=2, size_hint_y=None)
        for i in range(10):
            Contas.add_widget(Label(text='Conta', size_hint_y=None))
            Contas.add_widget(Label(text='Saldo', size_hint_y=None))
            Contas.add_widget(Label(text='Tipo', size_hint_y=None))
            Contas.add_widget(Button(text='Tornar\npadrão', size_hint_y=None))

        setContas.add_widget(Contas)

        
    