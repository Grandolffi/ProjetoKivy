import json
import os
from log import log

CAMINHO_ARQUIVO = "data/produtos.json" #Uma constante com o caminho onde os produtos serão salvos.

def carregar_produtos():
    if not os.path.exists("data"): #Nesse primeiro if, verifico se a pasta existe, se n existir a gente cria
        log.info("Produto_model -> carregar_produtos(): Pasta data não existe, criando...")
        os.makedirs("data")
    
    if not os.path.isfile(CAMINHO_ARQUIVO):  #Nesse segundo if, verifico se o json existe, se n existir cria com uma lista vazia
        log.info("Produto_model -> carregar_produtos(): Arquivo json não existe, criando...")
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f: #esse f significa que vamos chamar o arquivo aberto de F(apelido)
            json.dump([], f)

    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f: #Abrindo o arquivo .json em modo leitura ("r")
            produtos = json.load(f) #Usa json.load(f) para transformar o JSON em uma lista de produtos  
            log.info(f"Produto_model -> carregar_produtos(): {len(produtos)} produtos carregados do arquivo.")
            return produtos #retornando a lista de produtos
    except Exception as e:
        log.error(f"Produto_model -> carregar_produtos(): Erro ao carregar produtos: {e}") #log se der erro
        return [] #retornando lista vazia

def salvar_produtos(produtos): #Inicia a função que recebe uma lista de produtos
    log.info("Produto_model -> salvar_produtos(): Iniciando a função salvar_produto")
    try:
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f: #Abre o arquivo para escrita ("w"), o que sobrescreve o conteúdo.
            json.dump(produtos, f, indent=4, ensure_ascii=False) #json.dump() para gravar a lista em formato JSON./ indent=4: deixa o JSON legível (4 espaços)/ ensure_ascii=False: permite acentuação nas palavras
            log.info("Produto_model -> salvar_produtos(): Produtos salvos com sucesso.")
    except Exception as e:
        log.error(f"Produto_model -> salvar_produtos(): Erro ao salvar produtos: {e}")
