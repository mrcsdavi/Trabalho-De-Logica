from pysat.solvers import Glucose3
from pysat.formula import CNF
import matplotlib.pyplot as plt

class Npuzzle:

    dictSimbolos = {} # dicionario com os simbolos proposicionais

    matrizInicial = [
    #coluna  #1 #2 #3 
        [0, 1, 2], # linha 1 
        [3, 4, 5], # linha 2
        [6, 7, 8] # linha 3
    ]
    
    MatrizResultado = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]    

    def MapeamentoSimbolos(): # função para mapear simbolos
        estado = 1 # estado inicial
        qtdSimbolos = 0 # 81 possibilidades
        intMap = 0 # mapeamento dos simbolos para inteiros


        for coluna in range(3): 
            for linha in range(3): 
                intMap = intMap + 1

                simbolos = f"{estado}_P_{linha+1}_{coluna+1}_{Npuzzle.matrizInicial[linha][coluna]}" # criar simbolos

                Npuzzle.dictSimbolos[simbolos] = intMap # mapear para inteiros 

                
        for chave in Npuzzle.dictSimbolos:
                print(chave, ":", Npuzzle.dictSimbolos[chave])     

    def regrasEstado(): # regras para mapear cada estado

        pass


def main():
    Npuzzle.MapeamentoSimbolos()


if __name__ == "__main__":
    main()
