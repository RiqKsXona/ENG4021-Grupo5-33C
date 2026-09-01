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
            if escolha.lower() == el:
                return i
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
    return x/y

def calcula_resto(x, y):
    return x%y