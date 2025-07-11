from models.funcionario import Funcionario

class Gerente(Funcionario): #herda classe funcionario
    def __init__(self, nome, email, cpf):
        super().__init__(nome, email, cpf, cargo="gerente")
        self.permissoes = ["cadastro_usuario", "editar_usuario", "remover_usuario"]  # exemplo

    def to_dict(self):
        data = super().to_dict() #Reaproveita o dicionário da classe-mãe (Funcionario)
        data["tipo"] = "gerente"  # sobrescreve o tipo
        data["permissoes"] = self.permissoes
        return data

    @staticmethod
    def from_dict(data):
        gerente = Gerente(data.get("nome", ""), data.get("email", ""), data.get("cpf", ""))
        gerente.permissoes = data.get("permissoes", [])
        return gerente
