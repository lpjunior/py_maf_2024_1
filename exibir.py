def exibir_tarefas(tarefas):
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    for idx, tarefa in enumerate(tarefas):
        status = "Concluída" if tarefa["concluida"] else "Pendente"
        print("\nTarefa {}:".format(idx + 1))
        print("Título: {}".format(tarefa["titulo"]))
        print("Descrição: {}".format(tarefa["descricao"]))
        print("Status: {}".format(status))
