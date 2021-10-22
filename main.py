from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

#importa configurações gerais
#from appConfig import AppConfig

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        from telaPrincipal import Principal
        sm.add_widget(Principal(name="principal"))
        sm.current_screen.atualizaSaldo()
        from telaAdicionaGanho import AdicionaGanho
        sm.add_widget(AdicionaGanho(name="adicionaGanho"))
        from telaAdicionaRetirada import AdicionaRetirada
        sm.add_widget(AdicionaRetirada(name="adicionaRetirada"))
        from telaAdicionaConta import AdicionaConta
        sm.add_widget(AdicionaConta(name="adicionaConta"))
        from telaAlternaConta import AlternaConta
        sm.add_widget(AlternaConta(name="alternaConta"))
        return sm

if __name__ == "__main__":
    MyApp().run()