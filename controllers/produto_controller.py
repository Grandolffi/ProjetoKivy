from kivy.uix.boxlayout import BoxLayout #Base da interface: ´ Importa o BoxLayout, um layout em caixa (coluna ou linha) que empilha os elementos.´
from kivy.uix.label import Label # Importa o Label (texto na tela)
from kivy.uix.button import Button # importa o Button (botão de clicar).
from models.produto_model import carregar_produtos, salvar_produtos # Importa do model as funções que carrega a lista de produtos e salvar_produtos(lista) tudo em json
from kivy.clock import Clock  # Importando clock para usar no atualizar lista, para ele só ser carregado quando chamar a segunda parte do cod
from log import log

class ProdutoController(BoxLayout):
    def __init__(self, **kwargs): # (**kwargs) permite que o .kv passe propriedades como orientation: vertical
        super().__init__(**kwargs) # Chama a classe mae boxlayout 
        self.orientacao = 'vertical' # É orientação para o layout ser vertical porem pode ser reescrito no .kv
        self.produtos = carregar_produtos() # Carrega os produtos do arquivo .json e guarda na lista 
        log.info("Produto_Controller -> ProdutoController iniciado. Produtos carregados.")
        Clock.schedule_once(lambda dt: self.atualizar_lista(), 0) # Após carregar os produtos, monta a lista na tela, chamando a função atualizar_lista()



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
                self.produtos[self.index_edicao] = novo  # Substitui o produto antigo pelo novo
                del self.index_edicao  # Sai do modo edição
                self.ids["btn_add"].text = "Adicionar"  # Volta o texto do botão ao normal
            else:

                self.produtos.append(novo) #adiciona o dicionario(novo produto) na lista  de produtos
                log.info(f"Produto_Controller -> Produto adicionado: {novo}")

            salvar_produtos(self.produtos) #aqui salvamos toda a lista e volta pra o json incluindo o novo 
            #limpa os campos da input apos adicionar 

            self.ids.nome_input.text = ""
            self.ids.preco_input.text = ""
            self.ids.qtd_input.text = ""

            self.atualizar_lista() #Atualiza a lista na tela para mostrar o produto novo.
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



    def excluir_produto(self, index): #função de excluir
        log.info(f"Produto_Controller -> Entrando na função excluir_produto:, index: {index}")
        #Recebe o índice do produto na lista que deve ser removido
        if 0 <= index < len(self.produtos): #verifica se o index esta dentro da lista 
            removido = self.produtos.pop(index) #Remove o produto do índice informado e guarda na variável removido
            salvar_produtos(self.produtos) #Salva a nova lista sem o item.
            log.info(f"Produto_Controller -> Produto removido: {removido}")
            self.atualizar_lista() #Atualiza a lista da tela.
        else:
            log.error(f"Produto_Controller -> Índice inválido ao tentar excluir produto: {index}")



    def atualizar_lista(self):
        log.info("Produto_Controller -> Entrando na função atualizar_lista")
        self.ids.lista_produtos.clear_widgets() #Limpa a área da lista na tela (lista_produtos) antes de redesenhar.
        for index, produto in enumerate(self.produtos):
            box = BoxLayout(size_hint_y=None, height=30, spacing=5) #Cria uma nova linha horizontal com espaço fixo para mostrar o produto.

            #Adiciona as informações do produto (nome, preço, quantidade) em Labels com larguras proporcionais.            
            box.add_widget(Label(text=produto["nome"]))
            box.add_widget(Label(text=f'R$ {produto["preco"]}'))
            box.add_widget(Label(text=f'{produto["qtd"]} unid.'))

            btn_editar = Button(text="Editar", size_hint_x=None, width=70) #Cria um botão com o texto "Editar"
            btn_editar.bind(on_press=lambda instance, idx=index: self.preparar_edicao(idx)) #bind conecta o clique no botão à execução de uma função/idx=i: fixa o valor atual de i (índice do produto)./ self.preparar_edicao(idx): chama a função que preenche os campos com os dados do produto correspondente.
            box.add_widget(btn_editar)

            btn_excluir = Button(text='Excluir', size_hint_x=None, width=70) #Cria o botão “Excluir” 
            btn_excluir.bind(on_press=lambda btn, i=index: self.excluir_produto(i)) #lambda é uma função anônima Ela recebe dois argumentos:btn → o botão que foi clicado (obrigatório para o on_press) i=index → "fixa" o valor de index naquele momento
            box.add_widget(btn_excluir)

            self.ids.lista_produtos.add_widget(box) #Adiciona a box pronta na área da interface lista_produtos.



    def limpar_inputs(self): #função para limpar imputs
        log.info("Produto_Controller -> Entrando na função limpar_inputs")
        self.ids.nome_input.text = ""
        self.ids.preco_input.text = ""
        self.ids.qtd_input.text = ""