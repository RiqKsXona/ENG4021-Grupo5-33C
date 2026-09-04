import math

def calcula_divisao():
    numeros = input("digite primeiro o numerador de pois o denominador separados por virgula: ").split(",")
    div = int(numeros[0]) / int(numeros[1])
    return div
    
def calcula_divisao_inteira():
    numeros = input("digite primeiro o numerador de pois o denominador separados por virgula: ").split(",")
    div = int(numeros[0]) // int(numeros[1])
    return div

def calcula_resto():
    numeros = input("digite os numeros na ordem que voce deseja tirar o módulo separados por virgula: ").split(",")
    mod = int(numeros[0]) % int(numeros[1])
    return mod


def soma():
    numeros =input("digite os numeros que voce quer somar separados por virgula: ").split(",")
    soma = int(numeros[0]) + int(numeros[1])
    return soma


def subtrair():
    numeros =input("digite os numeros que voce quer subtrair separados por virgula: ").split(",")
    sub = int(numeros[0]) - int(numeros[1])
    return sub


def multiplicar():
    numeros = input("digite os numeros que voce quer multiplicar separados por virgula: ").split(",")
    prod = int(numeros[0]) * int(numeros[1])
    return prod

def raiz():
    numeros = input("digite primeiro o numero da base e depois o indice da raiz separados por virgula: ").split(",")
    rad = int(numeros[0]) ** (int(numeros[1])** -1)
    return rad


def potencia():
    numeros = input("digite primeiro o numero da base e depois o expoente separados por virgula: ").split(",")
    expo = int(numeros[0]) ** int(numeros[1])
    return expo

def porcentagem():
    numeros = input("digite primeiro o numero da porcentagem depois o numero principal separados por virgula: ").split(",")
    expo = (int(numeros[0])/100) * int(numeros[1])
    return expo

def main():

    operadores = ["somar","subtrair",
                "multiplicar","dividir","dividir int",
                "raiz","potencia", "porcentagem", "resto"]

    print(f"\n{ "===="*12}\n")
    for i,el in enumerate(operadores):
        if (i+1) % 3 == 0:
            print(f"| {el.upper()} |") 
        else:
            print(f"| {el.upper()}" , end=" |" )
    print(f"\n\n{ "===="*12}\n")
    print("Bem-Vindo!!")
    def choice(operadores):
        escolha = input("Escolha uma operação acima digitando-a exatamente como está escrito: ")
        for i,el in enumerate(operadores):
            if escolha.lower() == el:
                return i,True
        else:

            return False

    while True:
        ind, b = choice(operadores)
        if not b:
            print("\nEscolha inválida, por favor tente novamente!!")
        else:
                        if ind == 0:
                            s = soma()
                            print(f"A soma é: {s}")
                            break
            
                        elif ind == 1:
                            sub = subtrair()
                            print(f"A subtração resultante é: {sub}")
                            break
            
                        elif ind == 2:
                            m = multiplicar()
                            print(f"O produto resultante é: {m}")
                            break        
                    
                        elif ind == 3:
                            div = calcula_divisao()
                            print(f"O resultado da divisão é: {div:.2f}")
                            break  

                        elif ind == 4:
                            div = calcula_divisao_inteira()
                            print(f"O resultado da divisão é: {div}")
                            break   
            
                        elif ind == 5:
                            rad = raiz()
                            print(f"A raiz resultante é: {rad}")
                            break
            
                        elif ind == 6:
                            expo = potencia()
                            print(f"A potência resultante é: {expo}")
                            break

                        elif ind == 7:
                            porcent = porcentagem()
                            print(f"O resultado é: {porcent}")
                            break

                        elif ind == 8:
                            mod = calcula_resto()
                            print(f"O resto é: {mod}")
                            break
    


if __name__=="__main__":
    main()