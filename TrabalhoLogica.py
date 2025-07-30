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
        
        # qtdSimbolos = 0 # 81 possibilidades
        intMap = 1 # mapeamento dos simbolos para inteiros
            
        for estado in range(20): # mapeando para n estados, que no caso escolhido são 20 aqui=
            for posY in range(3): # posicao da coluna 
                for posX in range(3): # posicao da linha
                    for coluna in range(3): 
                        for linha in range(3): 
                            simbolos = f"{estado}_P_{posX+1}_{posY+1}_{Npuzzle.matrizInicial[linha][coluna]}" # criar simbolos

                            Npuzzle.dictSimbolos[simbolos] = intMap # mapear para inteiros 
                            intMap = intMap + 1

            
        for chave in Npuzzle.dictSimbolos:
                print(chave, "->", Npuzzle.dictSimbolos[chave])  

    # def regrasEstado(): # regras para mapear cada estado
    #     g = Glucose3        

    #     numPosicao = 0 
    #     for i in Npuzzle.dictSimbolos:
            
    #         verificaPosicao = Npuzzle.dictSimbolos[numPosicao] # verificar p/ todos os 0, todos os 1, etc (Clausula A) 

    #         for j in Npuzzle.dictSimbolos:
    #                 for k in Npuzzle.dictSimbolos:
    #                      simbolos = f"{estado}_P_{linha+1}_{coluna+1}_{Npuzzle.matrizInicial[linha][coluna]}" 
                    
                    
    #                 percorreSimbolos = Npuzzle.dictSimbolos[i] # Vai percorrer todas as posições (clausula B) 

    #                 g.add_clause([-verificaPosicao, -percorreSimbolos])
                
                    
    #                 posicao = posicao + 1
    #         verificaPosicao = Npuzzle.dictSimbolos[posicao]


def main():
    Npuzzle.MapeamentoSimbolos()
    #Npuzzle.regrasEstado()


if __name__ == "__main__":
    main()
