from kivy.uix.screenmanager import Screen

class HomeScreen(Screen):
    pass

class ProdutoScreen(Screen):
    pass

class MenuScreen(Screen):  
    def on_enter(self):
        from kivy.app import App
        print("Tipo de usuário atual:", App.get_running_app().tipo_usuario)
    pass

class ListaScreen(Screen):
    pass

class CadastroUsuarioScreen(Screen):  
    pass

class LoginUsuarioScreen(Screen):  
    pass

class ListarUsuariosScreen(Screen):
    pass