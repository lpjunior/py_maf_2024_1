# try, except, else, finally
def divide(x, y):
    try:
        resultado = x / y
    except ZeroDivisionError as e:
        print(f"Erro: Divisão por zero não é permitida. Erro: {e}")
    else:
        print(f"O resultado da divisão é {resultado}")


divide(10, 0)


def abrir_arquivo():
    try:
        file_path = "test.txt"
        arquivo = open(file_path, "r")
        conteudo = arquivo.read()
    except FileNotFoundError as e:
        print(f"não foi possível encontrar o arquivo. Erro: {e}")
    else:
        print(f"conteúdo do arquivo: {conteudo}")
    finally:
        try:
            arquivo.close()
        except NameError:
            pass
        print("Tentativa de fechar o arquivo, caso ele esteja aberto")


abrir_arquivo()
