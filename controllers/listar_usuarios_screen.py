import requests
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from services.firebase_config import FIREBASE_URL

Builder.load_file("views/cadastro_usuario.kv")


class ListarUsuariosScreen(Screen):
    def on_enter(self):
        self.carregar_usuarios()

    def carregar_usuarios(self):
        container = self.ids.usuarios_container
        container.clear_widgets()

        response = requests.get(f"{FIREBASE_URL}/usuarios.json")
        if response.status_code == 200 and response.json():
            dados = response.json()
            for uid, usuario in dados.items():
                info = f"{usuario.get('nome')} - {usuario.get('email')} - {usuario.get('tipo')}"
                from kivy.uix.label import Label
                container.add_widget(Label(text=info, color=(0,0,0,1), font_size=16, size_hint_y=None, height=30))
        else:
            from kivy.uix.label import Label
            container.add_widget(Label(text="Nenhum usuário encontrado", color=(0,0,0,1)))
