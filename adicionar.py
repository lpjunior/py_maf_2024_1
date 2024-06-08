def adicionar_tarefa(tarefas):
    titulo = input("Digite o titulo da tarefa: ")
    descricao = input("Digite a descricao da tarefa: ")

    tarefa = {
        "titulo": titulo,
        "descricao": descricao,
        "concluida": False
    }

    tarefas.append(tarefa)
    print(f"Tarefa '{titulo}' adicionada com sucesso!")
