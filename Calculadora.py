import math




def main():

    operadores = ["somar","subtrair",
                "multiplicar","dividir",
                "radiciação","exponenciação",
                "log","seno","cosseno", 
                "tangente","fatorial"]

    print(f"\n{ "===="*12}\n")
    for i,el in enumerate(operadores):
        if (i+1) % 3 == 0:
            print(f"{el.upper()}") 
        else:
            print(f"{el.upper()}," , end=" " )
    print(f"\n\n{ "===="*12}\n")
    print("Bem-Vindo!!")
    def choice():
        escolha = input("Escolha uma operação acima digitando-a exatamente como aparece: ")
        for i,el in enumerate(operadores):
            if i == 0:
                s = soma()
                print(f"A soma é: {s}")
                break

            elif i == 1:
                sub = subtrair()
                print(f"A subtração resultante é: {sub}")
                break

            elif i == 2:
                m = multiplicar()
                print(f"O produto resultante é: {m}")
                break        
        
            elif i == 3:
                div = calcula_divisao()
                print(f"O resultado da divisão é: {div}")
                break   

            elif i == 4:
                rad = raiz()
                print(f"A raiz resultante é: {rad}")
                break

            elif i == 5:
                expo = potencia()
                print(f"A potência resultante é: {expo}")
                break
            
            else:

                return None

    while True:
        ind = choice()
        if ind == None:
            print("\nEscolha inválida, por favor tente novamente!!")
        else:
            break
    


if __name__=="__main__":
    main()

def calcula_divisao(x, y):
    resultado=x/y
    return resultado

def calcula_resto(x, y):
    resultado=x%y
    return resultado
