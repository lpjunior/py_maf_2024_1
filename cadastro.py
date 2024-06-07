def cadastrar_aluno(alunos):
    nome = input("Digite o nome do aluno: ")
    idade = input("Digite a idade do aluno: ")
    cidade = input("Digite a cidade do aluno: ")
    nota1 = float(input("Digite a nota 1 do aluno: "))
    nota2 = float(input("Digite a nota 2 do aluno: "))
    aluno = {
        "nome": nome,
        "idade": idade,
        "cidade": cidade,
        "nota1": nota1,
        "nota2": nota2
    }
    alunos.append(aluno)
    print(f"Aluno {nome} cadastrado com sucesso!")
