# models/cliente.py

from models.pessoa import Pessoa

class Cliente(Pessoa):
    def __init__(self, nome, email, cpf):
        super().__init__(nome, email, cpf)

    def to_dict(self):
        data = super().to_dict()
        data["tipo"] = "cliente"
        return data

    @staticmethod
    def from_dict(data):
        return Cliente(
            data.get("nome", ""),
            data.get("email", ""),
            data.get("cpf", "")
        )
