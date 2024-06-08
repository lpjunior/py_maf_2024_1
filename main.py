# lista e tuplas
lista = [1, 2, 2, 3, 4, 5]  # lista
tupla = tuple(lista) # converte lista em tupla

print(lista)
print(tupla)

# dicionário
dicionario = {"nome": "João", "idade": 20}
print(dicionario)
print(dicionario["nome"])

# conjuntos
numeros = {1, 2, 2, 3, 4, 5}
print(numeros)

for numero in numeros:
    if numero == 2:
        print(numero)

lista_convertida_em_conjunto = set(lista)
print(lista_convertida_em_conjunto)