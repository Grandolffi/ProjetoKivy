from kivy.config import Config 

#Define a resolução da janela
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Builder #Builder, responsável por carregar o arquivo .kv com o layout visual.
from kivy.uix.screenmanager import ScreenManager #ScreenManager permite alternar entre telas diferentes no app
from controllers.produto_controller import ProdutoController
from controllers.cadastro_usuario_screen import CadastroUsuarioScreen
from views.telas import HomeScreen, ProdutoScreen, MenuScreen, ListaScreen, ListarUsuariosScreen
from controllers.lista_screen import ListaScreen
from controllers.login_usuario_screen import LoginUsuarioScreen

# Importa e registra o widget customizado antes de carregar o .kv
from kivy.factory import Factory # Factory permite registrar componentes personalizados (como IconButton
from widgets.icon_button import IconButton  
Factory.register('IconButton', cls=IconButton)
Factory.register('ProdutoController', cls=ProdutoController)

class ProdutoApp(App):
    tipo_usuario = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
         

    def build(self): #build() é chamado automaticamente pelo Kivy quando o app é iniciado.
        self.produto_controller = ProdutoController()
        Builder.load_file("views/main_view.kv") #Carrega o arquivo .kv, que define o layout visual.
        Builder.load_file("views/listar_usuarios.kv")
        sm = ScreenManager() #Cria o gerenciador de telas, que vai controlar a navegação.
        sm.add_widget(HomeScreen(name="home"))   # Tela inicial
        sm.add_widget(ProdutoScreen(name="produtos"))    # Tela de produtos
        sm.add_widget(MenuScreen(name="menu")) # Tela de menu
        sm.add_widget(ListaScreen(name="lista")) # Tela de lista de produtos
        sm.add_widget(CadastroUsuarioScreen(name="cadastro_usuario"))
        sm.add_widget(LoginUsuarioScreen(name="login_usuario"))
        sm.add_widget(ListarUsuariosScreen(name="listar_usuarios"))
        return sm

if __name__ == "__main__":
    ProdutoApp().run()
