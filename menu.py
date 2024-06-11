class Menu:
    @staticmethod
    def exibir():
        print(f"\nMenu Principal")
        print("1. Adicionar Produto")
        print("2. Exibir Produtos")
        print("3. Atualizar Produto")
        print("4. Excluir Produto")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")
        return opcao