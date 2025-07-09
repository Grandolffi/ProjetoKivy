from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager 
from views.telas import HomeScreen, ProdutoScreen 
from controllers.produto_controller import ProdutoController

class ProdutoApp(App):
    def build(self): #build() é chamado automaticamente pelo Kivy quando o app é iniciado.
        Builder.load_file("views/main_view.kv") #Carrega o arquivo .kv, que define o layout visual.
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))               # Tela inicial
        sm.add_widget(ProdutoScreen(name="produtos"))        # Tela de produtos
        return sm

if __name__ == "__main__":
    ProdutoApp().run()
