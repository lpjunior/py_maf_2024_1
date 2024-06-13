from abc import ABC, abstractmethod


class Animal(ABC):

    @abstractmethod
    def fazer_som(self):
        pass

    @abstractmethod
    def correr(self):
        pass


class Cachorro(Animal):
    def fazer_som(self):
        print("Au au")

    def correr(self):
        print("Correndo")


class Gato(Animal):
    def fazer_som(self):
        print("Miau")

    def correr(self):
        print("Correndo")


# Aplicando o polimorfismo
def emitir_som(animal):
    animal.fazer_som()


cachorro = Cachorro()
gato = Gato()

emitir_som(cachorro)
emitir_som(gato)
