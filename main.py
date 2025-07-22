import random
from puzzleSolverClass import PuzzleSolver


def random_move(state):
    x0, y0 = next((x, y) for x in range(3) for y in range(3) if state[x][y] == 0)
    moves = []

    if x0 > 0: moves.append('C')
    if x0 < 2: moves.append('B')
    if y0 > 0: moves.append('E')
    if y0 < 2: moves.append('D')

    a = random.choice(moves)

    new_state = [row[:] for row in state]
    if a == 'C':
        new_state[x0][y0] = state[x0-1][y0]
        new_state[x0-1][y0] = 0

    elif a == 'B':
        new_state[x0][y0] = state[x0+1][y0]
        new_state[x0+1][y0] = 0

    elif a == 'E':
        new_state[x0][y0] = state[x0][y0-1]
        new_state[x0][y0-1] = 0

    elif a == 'D':
        new_state[x0][y0] = state[x0][y0+1]
        new_state[x0][y0+1] = 0

    return new_state

def print_puzzle(state):
    for row in state:
        print(' '.join(str(x) for x in row))
    print()

def main():
    goal = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]
    
    initial = [row[:] for row in goal]
    num_moves = 10
    for _ in range(num_moves):
        initial = random_move(initial)
    
    print("Estado Inicial Gerado:")
    print_puzzle(initial)
    
    print("Estado Final (Objetivo):")
    print_puzzle(goal)
    
    solver = PuzzleSolver(initial, goal, max_steps=10)
    actions, steps = solver.solve()
    
    if actions:
        print(f"Solução encontrada em {steps} passos:")
        print("Sequência de Ações:", ' '.join(actions))
        
        current = initial
        print("\nPasso 0:")
        print_puzzle(current)
        
        for step, action in enumerate(actions, start=1):
            x0, y0 = next((x, y) for x in range(3) for y in range(3) if current[x][y] == 0)
            if action == 'C':
                current[x0][y0], current[x0-1][y0] = current[x0-1][y0], 0

            elif action == 'B':
                current[x0][y0], current[x0][y0] = current[x0][y0], 0

            elif action == 'E':
                current[x0][y0], current[x0][y0-1] = current[x0][y0-1], 0

            elif action == 'D':
                current[x0][y0], current[x0][y0+1] = current[x0][y0+1], 0

            print(f"Passo {step} (Ação: {action}):")
            print_puzzle(current)
    else:
        print("Não foi encontrada solução dentro do limite de passos.")

if __name__ == "__main__":
    main()