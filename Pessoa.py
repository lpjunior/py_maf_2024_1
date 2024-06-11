class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    # sobreescrita do metodo
    def __str__(self):
        return f'{self.nome} tem {self.idade} anos'

    def saudacao(self):
        return f'Olá, meu nome é {self.nome} e tenho {self.idade} anos.'


# Criando objeto da classe Pessoa
p1 = Pessoa('João', 20)

print(p1)

# Utilizando o método saudacao
print(p1.saudacao())
