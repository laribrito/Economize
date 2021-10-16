from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

#importa configurações gerais
from appConfig import AppConfig

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        from principal import Principal
        sm.add_widget(Principal(name="principal"))
        sm.current_screen.atualizaSaldo()
        from adicionaGanho import AdicionaGanho
        sm.add_widget(AdicionaGanho(name="adicionaGanho"))
        from adicionaRetirada import AdicionaRetirada
        sm.add_widget(AdicionaRetirada(name="adicionaRetirada"))
        from adicionaConta import AdicionaConta
        sm.add_widget(AdicionaConta(name="adicionaConta"))
        return sm

if __name__ == "__main__":
    MyApp().run()