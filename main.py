from menu import menu
from cadastro import cadastrar_aluno
from exibicao import exibir_alunos
from calculos import calcular_media


def main():
    alunos = []
    while True:
        escolha = menu()
        if escolha == 1:
            cadastrar_aluno(alunos)
        elif escolha == 2:
            exibir_alunos(alunos)
        elif escolha == 3:
            calcular_media(alunos)
        elif escolha == 4:
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
