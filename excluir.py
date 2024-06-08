def excluir_tarefa(tarefas):
    if not tarefas:
        print("Não há tarefas cadastradas")
        return

    try:
        indice = int(input("Digite o número da tarefa que você deseja excluir: ")) - 1
        if 0 <= indice < len(tarefas):
            tarefa_excluida = tarefas.pop(indice)
            print(f"Tarefa '{tarefa_excluida['titulo']}' excluída com sucesso!")
        else:
            print("Número da tarefa inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, digite um número.")
