from menu import Menu
from gerenciador_produto import GerenciadorProduto
from produto import Produto


def main():
    gerenciador_produto = GerenciadorProduto()
    while True:
        opcao = Menu.exibir()

        if opcao == '1':
            codigo = input("Digite o código do produto: ")
            nome = input("Digite o nome do produto: ")
            preco = float(input("Digite o preço do produto: "))
            quantidade = int(input("Digite a quantidade do produto: "))
            produto = Produto(codigo, nome, preco, quantidade)
            gerenciador_produto.adicionar_produto(produto)

        elif opcao == '2':
            gerenciador_produto.listar_produtos()

        elif opcao == '3':
            codigo = input("Digite o código do produto: ")
            nome = input("Digite o nome do produto: ")
            preco = float(input("Digite o preço do produto: "))
            quantidade = int(input("Digite a quantidade do produto: "))
            produto = Produto(codigo, nome, preco, quantidade)
            gerenciador_produto.atualizar_produto(produto)

        elif opcao == '4':
            codigo = input("Digite o código do produto: ")
            gerenciador_produto.remover_produto(codigo)

        elif opcao == '5':
            print("Saindo..")
            break

        else:
            print("Opção inválida!")


if __name__ == '__main__':
    main()
