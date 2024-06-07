peso = float(input('Qual o seu peso? (Kg): '))
altura = float(input('Qual a sua altura? (m): '))
imc = peso / (altura ** 2)
print('Seu IMC é de {:.2f}'.format(imc))
