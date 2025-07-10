from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from services.firebase_api import listar_produtos, excluir_produto_firebase
from log import log

class ListaScreen(Screen):
    def on_pre_enter(self):
        log.info("ListaScreen -> on_pre_enter chamado")
        self.atualizar_lista()

    def atualizar_lista(self, lista_id=None):
        log.info("Produto_Controller -> Entrando na função atualizar_lista")
        
        app = App.get_running_app()
        
        try:
            lista_screen = app.root.get_screen('lista')
            layout = lista_screen.ids.lista_produtos
        except Exception as e:
            log.error(f"Produto_Controller -> Erro ao acessar layout: {e}")
            return

        layout.clear_widgets()

        produtos_dict = listar_produtos()
        produtos = []
        if produtos_dict:
            for chave, dados in produtos_dict.items():
                dados["id"] = chave
                produtos.append(dados)

        #self.ids.lista_produtos.clear_widgets() #Limpa a área da lista na tela (lista_produtos) antes de redesenhar.
        for index, produto in enumerate(produtos):
            box = BoxLayout(size_hint_y=None, height=30, spacing=5) #Cria uma nova linha horizontal com espaço fixo para mostrar o produto.

            #Adiciona as informações do produto (nome, preço, quantidade) em Labels com larguras proporcionais.            
            box.add_widget(Label(text=produto["nome"]))
            box.add_widget(Label(text=f'R$ {produto["preco"]}'))
            box.add_widget(Label(text=f'{produto["qtd"]} unid.'))

            btn_editar = Button(text="Editar", size_hint_x=None, width=70) #Cria um botão com o texto "Editar"
            btn_editar.bind(on_press=lambda instance, p=produto: self.preparar_edicao(p)) #bind conecta o clique no botão à execução de uma função/idx=i: fixa o valor atual de i (índice do produto)./ self.preparar_edicao(idx): chama a função que preenche os campos com os dados do produto correspondente.
            box.add_widget(btn_editar)

            btn_excluir = Button(text='Excluir', size_hint_x=None, width=70) #Cria o botão “Excluir” 
            btn_excluir.bind(on_press=lambda btn, pid=produto["id"]: self.excluir_produto(pid)) #lambda é uma função anônima Ela recebe dois argumentos:btn → o botão que foi clicado (obrigatório para o on_press) i=index → "fixa" o valor de index naquele momento
            box.add_widget(btn_excluir)

            #self.ids.lista_produtos.add_widget(box) Adiciona a box pronta na área da interface lista_produtos.
            layout.add_widget(box)

    def excluir_produto(self, produto_id):
        log.info(f"ListaScreen -> Excluindo produto com ID: {produto_id}")
        excluir_produto_firebase(produto_id)
        self.atualizar_lista()

    def preparar_edicao(self, produto): #função de editar 
        log.info(f"ListaScreen -> Entrando na função preparar_edicao, produto: {produto}")
        app = App.get_running_app()
        produto_screen = app.root.get_screen("produtos")

        controller = produto_screen.ids.produto_controller

        controller.ids.nome_input.text = produto["nome"]
        controller.ids.preco_input.text = produto["preco"]
        controller.ids.qtd_input.text = produto["qtd"]

        controller.index_edicao = produto["id"]
        controller.ids["btn_add"].text = "Salvar Edição"

        app.root.current = "produtos"

