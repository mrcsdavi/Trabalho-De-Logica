from pysat.solvers import Glucose3
from pysat.formula import CNF
import matplotlib.pyplot as plt
import random

class Npuzzle:

    dictEstadoSimbolos = {}  # dicionário com os símbolos de posição das peças
    dictAcaoSimbolos = {}  # dicionário com os símbolos das ações de transição

    qtdEstados = 1  # você pode aumentar para testar mais passos de solução

    matrizInicial = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]

    MatrizResultado = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]

    def MapeamentoSimbolos():  # função para mapear símbolos
        intMap = 1  # contador para mapear os símbolos em inteiros

        # Mapear símbolos de posição das peças
        for estado in range(Npuzzle.qtdEstados):  # para cada estado
            for posY in range(3):  # coluna
                for posX in range(3):  # linha
                    for coluna in range(3):
                        for linha in range(3):
                            simbolos = f"{estado+1}_P_{posY+1}_{posX+1}_{Npuzzle.matrizInicial[linha][coluna]}"
                            Npuzzle.dictEstadoSimbolos[simbolos] = intMap
                            intMap += 1

        print("=== MAPEAMENTO DE ESTADOS ===")
        for chave in Npuzzle.dictEstadoSimbolos:
            print(chave, "->", Npuzzle.dictEstadoSimbolos[chave])

    def regrasEstado():
        g = Glucose3()

        for estado in range(Npuzzle.qtdEstados):
            for indicePos in range(9):
                valoresDict = [
                    valor
                    for chave, valor in Npuzzle.dictEstadoSimbolos.items()
                    if chave.startswith(f"{estado+1}_P_")
                        and int(chave.split("_")[2]) == (indicePos // 3 + 1)
                        and int(chave.split("_")[3]) == (indicePos % 3 + 1)
                ]

                g.add_clause(valoresDict)
                print(f"Estado {estado+1} | pos: {indicePos+1} | {' ∨ '.join(str(x) for x in valoresDict)}")

                for i in range(len(valoresDict)):
                    for j in range(i + 1, len(valoresDict)):  # evitar dupla contagem
                        g.add_clause([-valoresDict[i], -valoresDict[j]])
                        print(f"Estado {estado+1}; pos: {indicePos+1}; ¬{valoresDict[i]} ∨ ¬{valoresDict[j]}")

    def mapeamentoAcao():
        intMap = 1  # contador para mapear os símbolos em inteiros

        direcoes = [
            'C',
            'B',
            'E',
            'D'
        ]

        # Mapear símbolos de posição das peças
        for estado in range(Npuzzle.qtdEstados):  # para cada estado
            for i in range(3):  # coluna
                for j in range(3):  # linha
                    if Npuzzle.matrizInicial[i][j] == 0:
                        simbolos = f"{estado+1}_A_{random.choice(direcoes)}"

                        Npuzzle.dictAcaoSimbolos[simbolos] = intMap
                        intMap += 1

                        print(simbolos)


   # def regrasAcao():
        


def main():
    Npuzzle.MapeamentoSimbolos()
    Npuzzle.regrasEstado()
    Npuzzle.mapeamentoAcao()
    #Npuzzle.regrasAcao()


if __name__ == "__main__":
    main()
