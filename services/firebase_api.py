import requests

FIREBASE_URL = "https://kivymarket-default-rtdb.firebaseio.com"

def salvar_produto_firebase(produto):
    response = requests.post(f"{FIREBASE_URL}/produtos.json", json=produto)
    if response.status_code == 200:
        print("Produto salvo com sucesso no Firebase!")
    else:
        print("Erro ao salvar:", response.text)

def listar_produtos():
    response = requests.get(f"{FIREBASE_URL}/produtos.json")
    if response.status_code == 200:
        produtos = response.json()
        return produtos
    return {}

def excluir_produto_firebase(chave):
    response = requests.delete(f"{FIREBASE_URL}/produtos/{chave}.json")
    if response.status_code == 200:
        print("Produto excluído do Firebase.")
    else:
        print("Erro ao excluir produto:", response.text)
        
def editar_produto_firebase(chave, dados_atualizados):
    response = requests.put(f"{FIREBASE_URL}/produtos/{chave}.json", json=dados_atualizados)
    if response.status_code == 200:
        print("Produto atualizado com sucesso.")
    else:
        print("Erro ao editar produto:", response.text)
