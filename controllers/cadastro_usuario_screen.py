from kivy.uix.screenmanager import Screen
from models.funcionario import Funcionario
from models.gerente import Gerente
from models.cliente import Cliente
from kivy.lang import Builder
import requests
from log import log
from services.firebase_config import FIREBASE_URL

Builder.load_file("views/cadastro_usuario.kv")



class CadastroUsuarioScreen(Screen):
    def cadastrar_usuario(self):
        nome = self.ids.nome_input.text.strip()
        email = self.ids.email_input.text.strip()
        cpf = self.ids.cpf_input.text.strip()
        senha = self.ids.senha_input.text.strip()

        if not nome or not email or not cpf or not senha:
            print("Todos os campos devem ser preenchidos.")
            log.info("Todos os campos devem ser preenchidos.")
            return  # Interrompe o cadastro se faltar algo

        # Detectar tipo selecionado via ToggleButton
        if self.ids.tipo_cliente.state == "down":
            usuario = Cliente(nome, email, cpf)
        elif self.ids.tipo_funcionario.state == "down":
            usuario = Funcionario(nome, email, cpf, "Funcionário")
        elif self.ids.tipo_gerente.state == "down":
            usuario = Gerente(nome, email, cpf)
        else:
            usuario = Cliente(nome, email, cpf)  # padrão de segurança

        # Enviar para o Firebase
        data = usuario.to_dict()
        data["senha"] = senha
        response = requests.post(f"{FIREBASE_URL}/usuarios.json", json=data)

        if response.status_code == 200:
            print("Usuário cadastrado com sucesso!")
            # Limpar campos
            self.ids.nome_input.text = ""
            self.ids.email_input.text = ""
            self.ids.cpf_input.text = ""
            self.ids.senha_input.text = ""
            self.ids.tipo_cliente.state = "down"
            self.ids.tipo_funcionario.state = "normal"
            self.ids.tipo_gerente.state = "normal"
        else:
            print("Erro ao cadastrar:", response.text)