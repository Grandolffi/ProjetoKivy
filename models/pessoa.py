class Pessoa: #classe mae de funcionario 
    def __init__(self, nome, email, cpf):
        self.nome = nome
        self.email = email
        self.cpf = cpf

    def to_dict(self): #converte o objeto Pessoa para um dicionário, útil para salvar no Firebase.
        return {
            "tipo": "pessoa",  # pode ser sobrescrito por subclasses
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf
        }

    @staticmethod
    def from_dict(data): #recebe um dicionário (como o que vem do Firebase) e retorna um objeto Pessoa
        return Pessoa(data.get("nome", ""), data.get("email", ""), data.get("cpf", ""))