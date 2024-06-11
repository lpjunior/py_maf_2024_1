class ContaBancaria:
    def __init__(self, nome, numero, saldo=0):
        self.nome = nome
        self.numero = numero
        self.saldo = saldo

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
        else:
            print("Saldo insuficiente")

    def mostrar_saldo(self):
        print(f"Saldo atual: {self.saldo}")


# Criando objeto da classe ContaBancaria
conta1 = ContaBancaria('João', 123456, 1000)

# Usando os métodos da classe
conta1.depositar(500)
conta1.sacar(200)
conta1.mostrar_saldo()
conta1.sacar(200)
conta1.mostrar_saldo()
conta1.sacar(2000)  # Saldo insuficiente
