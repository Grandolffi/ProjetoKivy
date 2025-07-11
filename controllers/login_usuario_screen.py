import requests
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("views/login_usuario.kv")
FIREBASE_URL = "https://kivymarket-default-rtdb.firebaseio.com"

class LoginUsuarioScreen(Screen):
    def fazer_login(self):
        email = self.ids.email_input.text.strip()
        senha = self.ids.senha_input.text.strip()

        if not email or not senha:
            print("Email e senha são obrigatórios.")
            return

        response = requests.get(f"{FIREBASE_URL}/usuarios.json")
        if response.status_code == 200:
            usuarios = response.json()
            for key, usuario in usuarios.items():
                if usuario.get("email") == email and usuario.get("senha") == senha:
                    print("Login bem-sucedido!")
                    App.get_running_app().tipo_usuario = usuario["tipo"]
                    self.manager.current = "menu"
                    return

            print("Email ou senha inválidos.")
        else:
            print("Erro ao conectar com o servidor.")