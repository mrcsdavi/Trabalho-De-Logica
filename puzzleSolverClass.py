from pysat.solvers import Glucose3

class PuzzleSolver:
    def __init__(self, initial, goal, max_steps=30):
        self.initial = initial
        self.goal = goal
        self.max_steps = max_steps
        self.varmap = {}
        self.next_var = 1
        self.clauses = []

    def new_var(self, name):
        if name in self.varmap:
            return self.varmap[name]
        self.varmap[name] = self.next_var
        self.next_var += 1
        return self.next_var - 1

    def var_name(self, t, x, y, v):
        return f"P_{t}_{x}_{y}_{v}"

    def action_var_name(self, t, a):
        return f"A_{t}_{a}"

    def exactly_one(self, literals):
        self.clauses.append(literals)
        for i in range(len(literals)):
            for j in range(i + 1, len(literals)):
                self.clauses.append([-literals[i], -literals[j]])

    def add_initial_state(self):
        for x in range(3):
            for y in range(3):
                v = self.initial[x][y]
                var = self.new_var(self.var_name(0, x, y, v))
                self.clauses.append([var])

    def add_goal_state(self, step):
        for x in range(3):
            for y in range(3):
                v = self.goal[x][y]
                var = self.new_var(self.var_name(step, x, y, v))
                self.clauses.append([var])

    def add_state_constraints(self, t):
        for x in range(3):
            for y in range(3):
                literals = []
                for v in range(9):
                    literals.append(self.new_var(self.var_name(t, x, y, v)))
                self.exactly_one(literals)
        
        for v in range(9):
            literals = []
            for x in range(3):
                for y in range(3):
                    literals.append(self.new_var(self.var_name(t, x, y, v)))
            self.exactly_one(literals)

    def add_transition(self, t):
        actions = ['C', 'B', 'E', 'D']
        action_vars = [self.new_var(self.action_var_name(t, a)) for a in actions]
        self.exactly_one(action_vars)
        
        for a in actions:
            a_var = self.new_var(self.action_var_name(t, a))
            if a == 'C':
                positions = [(x, y) for x in [1, 2] for y in [0, 1, 2]]
            elif a == 'B':
                positions = [(x, y) for x in [0, 1] for y in [0, 1, 2]]
            elif a == 'E':
                positions = [(x, y) for x in [0, 1, 2] for y in [1, 2]]
            else:  # 'D'
                positions = [(x, y) for x in [0, 1, 2] for y in [0, 1]]
            
            for (x, y) in positions:
                p0_var = self.new_var(self.var_name(t, x, y, 0))
                premissa = [-a_var, -p0_var]
                
                if a == 'C':
                    x2, y2 = x - 1, y
                elif a == 'B':
                    x2, y2 = x + 1, y
                elif a == 'E':
                    x2, y2 = x, y - 1
                else:  # 'D'
                    x2, y2 = x, y + 1
                
                for v in range(9):
                    var_t_neighbor = self.new_var(self.var_name(t, x2, y2, v))
                    var_t1_current = self.new_var(self.var_name(t + 1, x, y, v))
                    self.clauses.append(premissa + [-var_t_neighbor, var_t1_current])
                    self.clauses.append(premissa + [-var_t1_current, var_t_neighbor])
                
                var_t1_neighbor_0 = self.new_var(self.var_name(t + 1, x2, y2, 0))
                self.clauses.append(premissa + [var_t1_neighbor_0])
                
                for i in range(3):
                    for j in range(3):
                        if (i, j) in [(x, y), (x2, y2)]:
                            continue
                        for v in range(9):
                            var_t_ij = self.new_var(self.var_name(t, i, j, v))
                            var_t1_ij = self.new_var(self.var_name(t + 1, i, j, v))
                            self.clauses.append(premissa + [-var_t_ij, var_t1_ij])
                            self.clauses.append(premissa + [-var_t1_ij, var_t_ij])

    def solve(self):
        for n_steps in range(self.max_steps + 1):
            self.varmap = {}
            self.next_var = 1
            self.clauses = []
            
            self.add_initial_state()
            self.add_state_constraints(0)
            
            for t in range(n_steps):
                self.add_state_constraints(t + 1)
                self.add_transition(t)
            
            self.add_goal_state(n_steps)
            
            solver = Glucose3()
            for clause in self.clauses:
                solver.add_clause(clause)
            
            if solver.solve():
                model = solver.get_model()
                actions_sequence = []
                for t in range(n_steps):
                    for a in ['C', 'B', 'E', 'D']:
                        a_var = self.new_var(self.action_var_name(t, a))
                        if a_var <= len(model) and model[a_var - 1] > 0:
                            actions_sequence.append(a)
                solver.delete()
                return actions_sequence, n_steps
            solver.delete()
        return None, None