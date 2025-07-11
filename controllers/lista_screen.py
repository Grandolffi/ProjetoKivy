from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from services.firebase_api import listar_produtos, excluir_produto_firebase
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from log import log

class ListaScreen(Screen):
    def on_pre_enter(self):
        log.info("ListaScreen -> on_pre_enter chamado")
        App.get_running_app().produto_controller.lista_screen = self
        self.atualizar_lista("")

    def atualizar_lista(self, lista_id=None):
        log.info("Produto_Controller -> Entrando na função atualizar_lista")
        
        app = App.get_running_app()
        
        #TRY Tenta acessar a tela lista e o layout com id lista_produtos. Se der erro, grava no log e sai
        try:
            lista_screen = app.root.get_screen('lista')
            layout = lista_screen.ids.lista_produtos
            filtro_nome = lista_screen.ids.campo_busca.text
        except Exception as e:
            log.error(f"Produto_Controller -> Erro ao acessar layout: {e}")
            return

        layout.clear_widgets() #Limpa todos os widgets que estavam antes na lista

        produtos_dict = listar_produtos() #Chama o Firebase para obter os produtos salvos.
        produtos = []
        if produtos_dict: #Converte o dicionário para uma lista de produtos com a chave id incluída em cada item.
            for chave, dados in produtos_dict.items():
                dados["id"] = chave
                produtos.append(dados)
        if filtro_nome:
            filtro_nome = filtro_nome.lower().strip()
            produtos = [p for p in produtos if filtro_nome in p["nome"].lower()]

        #self.ids.lista_produtos.clear_widgets() #Limpa a área da lista na tela (lista_produtos) antes de redesenhar.
        for index, produto in enumerate(produtos):
            box = BoxLayout(size_hint_y=None, height=30, spacing=5, padding=[10, 0]) #Cria uma nova linha horizontal com espaço fixo para mostrar o produto.

            ## Colunas de texto
            box.add_widget(Label(text=produto["nome"], color=(0.1, 0.1, 0.1, 1)))
            box.add_widget(Label(text=f'R$ {produto["preco"]}', color=(0.1, 0.1, 0.1, 1)))
            box.add_widget(Label(text=f'{produto["qtd"]} unid.', color=(0.1, 0.1, 0.1, 1)))

            # Coluna de ações
            acoes_box = BoxLayout(size_hint_x=None, width=120, spacing=5)

            btn_editar = Button(
                text="Editar", size_hint_x=None, width=55,
                background_normal='', background_color=(0, 0.5, 0.7, 1), color=(1, 1, 1, 1)
            )
            btn_editar.bind(on_press=lambda instance, p=produto: self.preparar_edicao(p))
            acoes_box.add_widget(btn_editar)

            btn_excluir = Button(
                text="Excluir", size_hint_x=None, width=55,
                background_normal='', background_color=(0.8, 0, 0, 1), color=(1, 1, 1, 1)
            )
            btn_excluir.bind(on_press=lambda instance, pid=produto["id"]: self.confirmar_exclusao(pid))
            acoes_box.add_widget(btn_excluir)

            # Aqui é o detalhe: adiciona o acoes_box dentro da linha (box)
            box.add_widget(acoes_box)

            # Adiciona a linha ao layout principal da lista
            layout.add_widget(box)

             # Linha separadora
            separador = Widget(size_hint_y=None, height=1)

            def desenhar_linha(*args):
                separador.canvas.clear()
                with separador.canvas:
                    Color(0.5, 0.5, 0.5, 0.5)  # cinza médio
                    Line(points=[0, 0, separador.width, 0], width=1)

            separador.bind(size=desenhar_linha)

            layout.add_widget(separador) #Adiciona essa linha logo após o produto na tela (separador visual).

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

    def confirmar_exclusao(self, produto_id): #Abre um popup de confirmação antes de excluir um produto.
    
        log.info(f"Solicitando confirmação para excluir produto: {produto_id}")

        box = BoxLayout(orientation='vertical', spacing=10, padding=10) 
 
        box.add_widget(Label(text="Tem certeza que deseja excluir este produto?", color=(0, 0, 0, 1))) #Adiciona o texto de confirmação dentro do popup.

        botoes = BoxLayout(spacing=10, size_hint_y=None, height=40)

        #Cria os dois botões: "Sim" com fundo vermelho, "Cancelar" com cinza.
        btn_sim = Button(text="Sim", background_color=(0.8, 0, 0, 1), color=(1, 1, 1, 1))
        btn_nao = Button(text="Cancelar", background_color=(0.6, 0.6, 0.6, 1), color=(0, 0, 0, 1))

        #Adiciona os botões na caixa horizontal.
        botoes.add_widget(btn_sim)
        botoes.add_widget(btn_nao)

        box.add_widget(botoes)

        popup = Popup(title="Confirmação", content=box,
                    size_hint=(None, None), size=(400, 200), auto_dismiss=False)

        btn_nao.bind(on_release=popup.dismiss) #Se o usuário clicar em "Cancelar", fecha o popup.
        btn_sim.bind(on_release=lambda x: self._confirmar_exclusao_real(produto_id, popup)) #Se o usuário clicar em "Sim", chama a função que realmente exclui o produto.

        popup.open()

    def _confirmar_exclusao_real(self, produto_id, popup): #Realiza a exclusão após confirmação do popup.
        log.info(f"Produto confirmado para exclusão: {produto_id}") 
        popup.dismiss() #Fecha o popup.
        self.excluir_produto(produto_id)

