from pysat.solvers import Glucose3
import random

class Npuzzle:
    g = Glucose3()

    dictEstadoSimbolos = {}  # dicionário com os símbolos de posição das peças
    dictAcaoSimbolos = {}  # dicionário com os símbolos das ações de transição
    direcoes = [ # direções para os simbolos de transicao
            'C',
            'B',
            'E',
            'D'
        ]


    qtdEstados = 1  # você pode aumentar para testar mais passos de solução

    matrizInicial = None

    MatrizResultado = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]

    def gerar_matriz_aleatoria():
        numeros = list(range(9)) # Cria uma lista com todos os números de 0 a 8
        random.shuffle(numeros)  # Divide em 3 linhas de 3 elementos cada
        matriz = [numeros[i*3:(i+1)*3] for i in range(3)]
        return matriz

    def MapeamentoSimbolos():  # função para mapear símbolos
        intMap = 1  # contador para mapear os símbolos em inteiros
        if Npuzzle.matrizInicial is None:
            Npuzzle.matrizInicial = Npuzzle.gerar_matriz_aleatoria()

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

        for estado in range(Npuzzle.qtdEstados):
            for indicePos in range(9):
                valoresDict = [
                    valor
                    for chave, valor in Npuzzle.dictEstadoSimbolos.items()
                    if chave.startswith(f"{estado+1}_P_")
                        and int(chave.split("_")[2]) == (indicePos // 3 + 1)
                        and int(chave.split("_")[3]) == (indicePos % 3 + 1)
                ]

                Npuzzle.g.add_clause(valoresDict)
                print(f"Estado {estado+1} | pos: {indicePos+1} | {' ∨ '.join(str(x) for x in valoresDict)}")

                for i in range(len(valoresDict)):
                    for j in range(i + 1, len(valoresDict)):  # evitar dupla contagem
                        Npuzzle.g.add_clause([-valoresDict[i], -valoresDict[j]])
                        print(f"Estado {estado+1}; pos: {indicePos+1}; ¬{valoresDict[i]} ∨ ¬{valoresDict[j]}")

    def mapeamentoAcao():
        # começa a numeração depois do último símbolo de estado
        intMap = 1

        for estado in range(Npuzzle.qtdEstados):  # para cada estado
            for i in range(3):  # coluna
                for j in range(3):  # linha
                    if Npuzzle.matrizInicial[i][j] == 0:
                        for direcao in Npuzzle.direcoes:
                            simbolos = f"{estado+1}_A_{direcao}"
                            Npuzzle.dictAcaoSimbolos[simbolos] = intMap
                            intMap += 1
                            

        print("=== MAPEAMENTO DE AÇÕES ===")
        for chave, valor in Npuzzle.dictAcaoSimbolos.items():
            print(chave, "->", valor)

    def regraAcao():
        g = Glucose3()

        for estado in range(Npuzzle.qtdEstados):
            for posY in range(3):  # coluna
                for posX in range(3):  # linha
                    for coluna in range(3):
                        for linha in range(3):
               
                            # vai rodar na posicao ESTADO_P_1_1_? e até encontrar o 0
                            if ((posY+1 == 1 and posX+1 == 1) and Npuzzle.matrizInicial[linha][coluna] == 0): 
                                pos0 = f"{estado+1}_P_{posY+1}_{posX+1}_{Npuzzle.matrizInicial[linha][coluna]}" 
                                salvarPos0 = pos0 # salvando a posição do 0

                                for i in Npuzzle.direcoes: 
                                    acao = f"{estado+1}_A_{i}" # para comparar com o dicionario das acoes com as direções diferentes

                                    # posicao 1_2:
                                    if (i == 'E'):
                                        # if para comparar com o dicionario das acoes com as direções diferentes
                                        if acao in Npuzzle.dictAcaoSimbolos:
                                            # roda esse for para ver se tem algo igual no dicionario dos simbolos
                                            for linha1 in range(3):
                                                for coluna1 in range(3):
                                                    # posNum é a posicao, por exemplo, 1_2 que nao sem o 0
                                                    posNum = f"{estado+1}_P_1_2_{Npuzzle.matrizInicial[linha1][coluna1]}"

                                                    if posNum in Npuzzle.dictEstadoSimbolos and Npuzzle.dictEstadoSimbolos[posNum]:

                                                        # tenho q pegar o valor do int, e pelo int, trocar a chave do 0 pelo numero e requerido e vice versa

                                                        # Obter inteiros dos símbolos
                                                        int_posNum = Npuzzle.dictEstadoSimbolos[posNum]
                                                        int_pos0 = Npuzzle.dictEstadoSimbolos[pos0]

                                                        int_acao = Npuzzle.dictAcaoSimbolos[acao]

                                                        pos0 = posNum 
                                                        posNum = salvarPos0 

                                                        num0 = pos0.split("_")[-1]   
                                                        numNum = posNum.split("_")[-1]  

                                                        # Crie as novas chaves para o próximo estado (estado+1)
                                                        novaPos0 = f"{estado+1}_P_{pos0.split('_')[2]}_{pos0.split('_')[3]}_{num0}"
                                                        novaPosNum = f"{estado+1}_P_{posNum.split('_')[2]}_{posNum.split('_')[3]}_{numNum}"

                                                        int_novaPos0 = Npuzzle.dictEstadoSimbolos[novaPos0]
                                                        int_novaPosNum = Npuzzle.dictEstadoSimbolos[novaPosNum]
                
                                                        Npuzzle.g.add_clause([-int_posNum, -int_pos0, -int_acao, int_novaPos0])
                                                        Npuzzle.g.add_clause([-int_posNum, -int_pos0, -int_acao, int_novaPosNum])

                                                    # atualizar o estado dos dois alterados no dicionario
                                                    # tem que dar um break

                                    # # posicao 2_1:
                                    # elif (i == 'C'):
                                    #     if Npuzzle.dictAcaoSimbolos == chave":

                                    #     pos2_1 = f"{estado+1}_P_2_1_{Npuzzle.matrizInicial[linha][coluna]}"
                                    
                                    # # se houver movimento impossivel
                                    # else:
                                    #     pass

                                    # # trocar posições 

                                    


                                    # simbolos = f"{estado+1}_P_{posY+1}_{posX+1}_{Npuzzle.matrizInicial[linha][coluna]}"

    
                                # # 1_2 = 0
                                # for i in Npuzzle.direcoes:
                                #         chave = f"{estado+1}_A_{i}"


                                #         if (i == 'E') : 
                                            
                                            
                                #         if (i == 'B'):


                                #         if (i == 'D'):

                                    

                                # # 1_3 == 0 
                                # for i in Npuzzle.direcoes:
                                #     chave = f"{estado+1}_A_{i}"

                                #     if (i == 'E'): 
                                            
                                #     if (i == 'B'):


                                # # 2_1 == 0
                                # for i in Npuzzle.direcoes:
                                #     chave = f"{estado+1}_A_{i}"


                                #     if (i == 'C'): 
                                            
                                #     if (i == 'D'): 

                                #     if (i == 'B'):

                                #     # 2_2 == 0
                                    

                                # for i in Npuzzle.direcoes:
                                #     chave = f"{estado+1}_A_{i}"

                                #     if (i == 'E'): 
                                            
                                #     if (i == 'C'): 

                                #     if (i == 'D'):

                                #     if (i == 'B'):

                                # # 2_3 == 0
                                # for i in Npuzzle.direcoes:
                                #     chave = f"{estado+1}_A_{i}"

                                #     if (i == 'C'): 
                                            
                                #     if (i == 'E'): 

                                #     if (i == 'B'):

                                #     # 3_1 == 0
                                # for i in Npuzzle.direcoes:
                                #     chave = f"{estado+1}_A_{i}"

                                #     if (i == 'C'): 
                                            
                                #     if (i == 'D'): 

                                #     # 3_2 == 0
                                # for i in Npuzzle.direcoes:
                                #     chave = f"{estado+1}_A_{i}"

                                #     if (i == 'E'): 
                                            
                                #     if (i == 'C'):
                                                
                                #     if (i == 'D'): 


                                # # 3_3 == 0
                                # for i in Npuzzle.direcoes:
                                #     chave = f"{estado+1}_A_{i}"

                                #     if (i == 'E'): 
                                            
                                #     if (i == 'C'):
                                

                                
def main():
    

    Npuzzle.MapeamentoSimbolos()
    Npuzzle.regrasEstado()
    Npuzzle.mapeamentoAcao()
    Npuzzle.regraAcao()

    print(Npuzzle.g.solve())
    print(Npuzzle.g.get_model())


if __name__ == "__main__":
    main()
