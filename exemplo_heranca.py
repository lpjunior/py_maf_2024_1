class Pessoa:
    def __init__(self, nome, sobrenome, idade):
        self._nome = nome + ' ' + sobrenome
        self._idade = idade

    def __str__(self):
        return f'Nome: {self._nome}, Idade: {self._idade}'

    def saudacao(self):
        print(f'Olá, {self._nome}!')


class Aluno(Pessoa):  # Aluno é subclasse (filha) de Pessoa(superclasse)
    def __init__(self, nome, sobrenome, idade, matricula):
        super().__init__(nome, sobrenome, idade)
        self.__matricula = matricula

    def __str__(self):
        return f'Nome: {self._nome}, Idade: {self._idade}, Matricula: {self.__matricula}'

    def saudacao(self):
        super().saudacao()
        print(f'Sou um aluno!')


class Professor(Pessoa):
    def __init__(self, nome, sobrenome, idade, salario):
        super().__init__(nome, sobrenome, idade)
        self.__salario = salario

    def __str__(self):
        return f'Nome: {self._nome}, Idade: {self._idade}, Salario: {self.__salario}'

    def saudacao(self):
        super().saudacao()
        print(f'Sou um professor!')


a1 = Aluno('João', 'Silva', 20, '123456')
p1 = Professor('Maria', 'Santos', 40, 5000)
print(a1)
print(p1)
