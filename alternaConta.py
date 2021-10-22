from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from functools import partial
from kivy.properties import ObjectProperty

Builder.load_file("telas/alternaConta.kv")

#importa o banco de dados
from model import db

#importa as configurações gerais do sistema
from appConfig import AppConfig

class AlternaConta(Screen):    
    raiz = []
    box = []

    def tornaPadrao(self, *args):
        AppConfig.set_config("contaPadrao", args[1])
        self.manager.current="principal"
        self.manager.transition.direction = "right"
        self.manager.current_screen.setMensagem.text = 'Conta padrão alterada com sucesso!'
        self.manager.current_screen.atualizaSaldo()

    def exibirContas(self):
        rolagem = ScrollView(pos_hint={"top": 0.9}, size_hint_y=0.8)

        layout = BoxLayout(size_hint_y=None)

        try:
            #limpa o ScrollView
            self.raiz.clear_widgets()
        except AttributeError:
            #é a primeira vez que a tela é aberta
            # não precisa de limpeza
            pass

        try:
            #limpa o BoxLayout
            self.box.clear_widgets()
        except AttributeError:
            #é a primeira vez que a tela é aberta
            # não precisa de limpeza
            pass
        
        contas = db.retorna_contas()
        quant = len(contas)

        #adiciona os widgets à tela
        if quant == 0:
            layout.add_widget(Label(text="Não há contas cadastradas ainda", size_hint_y=None))
        else:
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
                btn.bind(on_press=partial(self.tornaPadrao, ind, conta[1]))
                Contas.add_widget(btn)

                
            layout.add_widget(Contas)    
            layout.add_widget(Label(text="Fim", size_hint_y=None))

        self.box = layout
        rolagem.add_widget(layout)
        #armazena o objeto ScrollView no atributo raiz
        self.raiz = rolagem
        self.add_widget(rolagem)

        
    