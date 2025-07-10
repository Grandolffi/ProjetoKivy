from kivy.uix.boxlayout import BoxLayout # Importa o BoxLayout, um layout em caixa (coluna ou linha) que empilha os elementos.
from kivy.uix.label import Label # Importa o Label (texto na tela)
from kivy.uix.button import Button # importa o Button (botão de clicar).
from kivy.clock import Clock  # Importando clock para usar no atualizar lista, para ele só ser carregado quando chamar a segunda parte do cod
from services.firebase_api import salvar_produto_firebase, listar_produtos, excluir_produto_firebase, editar_produto_firebase
from log import log
from kivy.app import App

class ProdutoController(BoxLayout):
    def __init__(self, **kwargs): # (**kwargs) permite que o .kv passe propriedades como orientation: vertical
        super().__init__(**kwargs) # Chama a classe mae boxlayout 
        self.orientacao = 'vertical' # É orientação para o layout ser vertical porem pode ser reescrito no .kv
        #self.produtos = carregar_produtos() #antigo json, não usa mais
        self.carregar_produtos_firebase()
        log.info("Produto_Controller -> ProdutoController iniciado. Produtos carregados.")

    def adicionar_produto(self): #Função chamada quando o botão "Adicionar" é clicado.
        log.info(f"Produto_Controller -> Entrando na função adicionar_produto:")
        nome = self.ids.nome_input.text #Pega o texto dos inputs do .kv com os IDs: nome_input
        preco = self.ids.preco_input.text #id inputs .kv: preco_input
        qtd = self.ids.qtd_input.text #id inputs .kv: qtd_input

        if nome and preco and qtd: #if para verificar se tenho todos os dados 
            novo = {
                "nome": nome,
                "preco": preco,
                "qtd": qtd
            } #nessa linha de cima criei um dicionario que representa o produto

            if hasattr(self, 'index_edicao'): #Verifica se aquele atributo já existe dentro do objeto self
                log.info(f"Produto_Controller -> Salvando edição no índice: {self.index_edicao}")
                chave = self.index_edicao
                editar_produto_firebase(chave, novo)
                del self.index_edicao
                self.ids["btn_add"].text = "Adicionar"
            else:

                salvar_produto_firebase(novo)  # Adiciona no Firebase
                log.info(f"Produto_Controller -> Produto adicionado: {novo}")
                
            #limpa os campos da input apos adicionar 

            self.limpar_inputs()

            self.carregar_produtos_firebase()  # Recarrega a lista do Firebase, Atualiza a lista na tela para mostrar o produto novo.
            
        else:
            log.warning("Produto_Controller -> Tentativa de adicionar produto com campos vazios.")


    def preparar_edicao(self, index): #função de editar 
        log.info(f"Produto_Controller -> Entrando na função preparar_edicao, index: {index}")
        produto = self.produtos[index]
        self.ids.nome_input.text = produto["nome"]
        self.ids.preco_input.text = produto["preco"]
        self.ids.qtd_input.text = produto["qtd"]
        self.index_edicao = index
        self.ids["btn_add"].text = "Salvar Edição"

    def carregar_produtos_firebase(self):
        produtos_dict = listar_produtos()
        self.produtos = []
        if produtos_dict:
            for chave, dados in produtos_dict.items():
                dados["id"] = chave
                self.produtos.append(dados)

    def limpar_inputs(self): #função para limpar imputs
        log.info("Produto_Controller -> Entrando na função limpar_inputs")
        self.ids.nome_input.text = ""
        self.ids.preco_input.text = ""
        self.ids.qtd_input.text = ""