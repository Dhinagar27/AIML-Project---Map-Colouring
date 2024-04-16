import time

from csp.problem import Problem
from csp.solvers import MinConflictsSolver, RecursiveBacktrackingSolver

regions = ['BAV', 'BAD', 'SAAR', 'RHINE', 'WEST', 'HES', 'THUR', 'SAX', 'SAXAN', 'LOWSAX', 'HOLS', 'BRAND', 'MECK']
borders = [('BAV', 'BAD'), ('BAV', 'HES'), ('BAV', 'THUR'), ('BAV', 'SAX'), ('BAD', 'HES'), ('BAD', 'RHINE'),
           ('SAAR', 'RHINE'), ('RHINE', 'HES'), ('RHINE', 'WEST'), ('WEST', 'HES'), ('WEST', 'LOWSAX'), ('HES', 'THUR'),
           ('HES', 'LOWSAX'), ('THUR', 'SAX'), ('THUR', 'LOWSAX'), ('THUR', 'SAXAN'), ('SAX', 'SAXAN'), ('SAX', 'BRAND'),
           ('SAXAN', 'BRAND'), ('SAXAN', 'LOWSAX'), ('LOWSAX', 'BRAND'), ('LOWSAX', 'HOLS'), ('LOWSAX', 'MECK'),
           ('HOLS', 'MECK'), ('BRAND', 'MECK')]

colors = ["red", "blue", "green", "yellow"]


def check_border(variables, *args):
    zipped = list(zip(variables, args))
    return zipped[0][1] != zipped[1][1]

def solve_csp(solver):
    problem = Problem(solver)
    problem.add_variables(regions, colors)
    for node in regions:
        borders_per_node = [borders[index] for (index, a_tuple) in enumerate(borders) if a_tuple[0] == node]
        if borders_per_node:
            for border in borders_per_node:
                problem.add_constraint(check_border, list(border))

    start_time = time.time()
    problem.get_solution()
    end_time = (time.time() - start_time)
    print(f"Solution with {solver.get_description()} took {end_time} sec and {solver.counter} checks")
    problem.plot_map(borders)

if __name__ == "__main__":
    solvers = [RecursiveBacktrackingSolver(forwardcheck=False), RecursiveBacktrackingSolver(forwardcheck=True), MinConflictsSolver()]
    for solver in solvers:
        solve_csp(solver)