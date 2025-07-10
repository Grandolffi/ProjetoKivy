from kivy.config import Config 

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from controllers.produto_controller import ProdutoController
from views.telas import HomeScreen, ProdutoScreen, MenuScreen, ListaScreen
from controllers.lista_screen import ListaScreen

# Importa e registra o widget customizado antes de carregar o .kv
from kivy.factory import Factory
from widgets.icon_button import IconButton  # Caminho correto do seu componente
Factory.register('IconButton', cls=IconButton)
Factory.register('ProdutoController', cls=ProdutoController)

class ProdutoApp(App):
    def build(self): #build() é chamado automaticamente pelo Kivy quando o app é iniciado.
        Builder.load_file("views/main_view.kv") #Carrega o arquivo .kv, que define o layout visual.
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))   # Tela inicial
        sm.add_widget(ProdutoScreen(name="produtos"))    # Tela de produtos
        sm.add_widget(MenuScreen(name="menu")) # Tela de menu
        sm.add_widget(ListaScreen(name="lista"))
        return sm

if __name__ == "__main__":
    ProdutoApp().run()
