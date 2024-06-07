import os


def executar_script(caminho):
    with open(caminho, 'r', encoding='utf-8-sig') as file:
        exec(file.read())


def menu():
    while True:
        print("\nMenu Principal")
        print("1. Hello")
        print("2. Operações de Entrada/Saída")
        print("3. Conversor de temperatura")
        print("4. Calculadora de IMC")
        print("0. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            executar_script('hello.py')
        elif escolha == '2':
            executar_script('io_operations.py')
        elif escolha == '3':
            executar_script('temperature_converter.py')
        elif escolha == '4':
            executar_script('imc_calculator.py')
        elif escolha == '0':
            print('Saindo...')
            break
        else:
            print('Opção inválida! Tente novamente.')


if __name__ == '__main__':
    menu()
