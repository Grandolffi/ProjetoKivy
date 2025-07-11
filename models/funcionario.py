from models.pessoa import Pessoa

class Funcionario(Pessoa): #funcionario é a classe filha da classe pessoa
    def __init__(self, nome, email, cpf, cargo):
        super().__init__(nome, email, cpf) #indica que esta herdando atributos da classe ame
        self.cargo = cargo  # exemplo: "caixa", "estoquista", "gerente"

    def to_dict(self): #converte o objeto Pessoa para um dicionário, útil para salvar no Firebase.
        data = super().to_dict() #Chama o método to_dict da classe Pessoa
        data["tipo"] = "funcionario"  # sobrescreve o tipo
        data["cargo"] = self.cargo
        return data

    @staticmethod
    def from_dict(data):
        return Funcionario(data.get("nome", ""), data.get("email", ""), data.get("cpf", ""), data.get("cargo", ""))
