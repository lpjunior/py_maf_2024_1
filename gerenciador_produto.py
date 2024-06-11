from validador_produto import ValidadorProduto


class GerenciadorProduto:
    def __init__(self):
        self.produtos = []

    def adicionar_produto(self, produto):
        try:
            ValidadorProduto.validar(produto)
            self.produtos.append(produto)
            print(f"Produto '{produto.nome}' adicionado com sucesso!")
        except ValueError as e:
            print(f"Erro ao adicionar produto: {e}")

    def listar_produtos(self):
        try:
            if len(self.produtos) == 0:
                raise ValueError("Nenhum produto cadastrado")
            for idx, produto in enumerate(self.produtos):
                print(f"{idx + 1}. {produto}")
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")

    def buscar_produto(self, codigo):
        try:
            for produto in self.produtos:
                if produto.codigo == codigo:
                    return produto
            raise ValueError(f"Produto com código {codigo} não encontrado")
        except Exception as e:
            print(f"Erro ao buscar produto: {e}")

    def remover_produto(self, codigo):
        try:
            produto = self.buscar_produto(codigo)
            self.produtos.remove(produto)
            print(f"Produto '{produto.nome}' removido com sucesso!")
        except Exception as e:
            print(f"Erro ao remover produto: {e}")

    def atualizar_produto(self, produto):
        try:
            ValidadorProduto.validar(produto)
            produto_localizado = self.buscar_produto(produto.codigo)
            produto_localizado.atualizar(produto.nome, produto.preco, produto.quantidade)
            print(f"Produto '{produto.nome}' atualizado com sucesso!")
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")
