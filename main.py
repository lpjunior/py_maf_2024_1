from menu import menu
from adicionar import adicionar_tarefa
from exibir import exibir_tarefas
from marcar_concluida import marcar_tarefa_concluida
from excluir import excluir_tarefa


def main():
    tarefas = []
    while True:
        opcao = menu()
        if opcao == '1':
            adicionar_tarefa(tarefas)
        elif opcao == '2':
            exibir_tarefas(tarefas)
        elif opcao == '3':
            marcar_tarefa_concluida(tarefas)
        elif opcao == '4':
            excluir_tarefa(tarefas)
        elif opcao == '5':
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")


if __name__ == '__main__':
    main()
