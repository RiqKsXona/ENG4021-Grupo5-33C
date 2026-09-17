def calcula_soma(x, y): 
    pass

def calcula_subtracao(x, y):
    pass

def calcula_multiplicacao(x, y):
    pass

def calcula_divisao(x, y):
    pass

def calcula_exponenciacao(x, y):
    pass

def calcula_radiciacao(x, y):
    pass

def calcula_divisao_inteira(x, y):
    pass

def calcula_resto(x, y):
    pass



#Bloco principal

numero_da_operacao = KeyboardInterrupt(input('''Escolha a operação desejada:))
1 - Soma
2 - Subtração
3 - Multiplicação
4 - Divisão
5- Exponenciação
6- Radiciação
7- Divisão inteira
8- Resto
0- Sair
'''))

if numero_da_operacao == 0:
    print('Saiu do programa')
elif numero_da_operacao > 0 and numero_da_operacao <= 8:
    x = float(input('Digite o primeiro número: '))
    y = float(input('Digite o segundo número: '))

    if numero_da_operacao == 1:
        resultado = calcula_soma(x, y)
        print(f'O resultado da soma é: {resultado}')

    elif numero_da_operacao == 2:
        resultado = calcula_subtracao(x, y)
        print(f'O resultado da subtração é: {resultado}')

    elif numero_da_operacao == 3:
        resultado = calcula_multiplicacao(x, y)
        print(f'O resultado da multiplicação é: {resultado}')

    elif numero_da_operacao == 4:
     resultado = calcula_divisao(x, y)
     print(f'O resultado da divisão é: {resultado}')

    elif numero_da_operacao == 5:
        resultado = calcula_exponenciacao(x, y)
        print(f'O resultado da exponenciação é: {resultado}')

    elif numero_da_operacao == 6:
        resultado = calcula_radiciacao(x, y)
        print(f'O resultado da radiciação é: {resultado}')

    elif numero_da_operacao == 7:
        resultado = calcula_divisao_inteira(x, y)
        print(f'O resultado da divisão inteira é: {resultado}')

    elif numero_da_operacao == 8:
        resultado = calcula_resto(x, y)
        print(f'O resultado do resto é: {resultado}')

else:
    print('Operação inválida, digite um numero de 0 a 8')

