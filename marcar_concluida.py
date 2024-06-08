def marcar_tarefa_concluida(tarefas):
    if not tarefas:
        print("Não há tarefas cadastradas")
        return tarefas

    try:  # Código que pode gerar exceção
        indice = int(input("Digite o número da tarefa que deseja marcar como concluída: ")) - 1
        if 0 <= indice < len(tarefas):
            tarefas[indice]["concluida"] = True
            print(f"Tarefa '{tarefas[indice]['titulo']}' marcada como concluída!")
        else:
            print("Número da tarefa inválido.")
    except ValueError:  # Tratamento de exceção
        print("Entrada inválida. Por favor, digite um número.")
