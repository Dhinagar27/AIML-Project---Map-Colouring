import networkx as nx
import matplotlib.pyplot as plt

from csp.constraint import Constraint
from csp.variables import Domain


class Problem(object):
    def __init__(self, solver=None):
        self._solver = solver
        self._constraints = []
        self._variables = {}

    def add_variable(self, variable, domain):
        domain = Domain(domain)
        self._variables[variable] = domain

    def add_variables(self, variables, domain):
        self.all_variables = variables
        for variable in variables:
            self.add_variable(variable, domain)

    def add_constraint(self, constraint, variables=None):
        constraint = Constraint(constraint)
        self._constraints.append((constraint, variables))

    def plot_map(self, edges):
        G = nx.Graph()
        G.add_nodes_from(self.all_variables)
        G.add_edges_from(edges)
        color_map = {}
        for node in self.all_variables:
            color_map[node] = self._solution[node]
        node_colors = [color_map.get(node) for node in G.nodes()]

        plt.title(self._solver.get_description())
        layout = nx.spring_layout(G, k = 1, seed=112)
        nx.draw(G, pos=layout, with_labels=True, node_color=node_colors, node_size=2000, cmap=plt.cm.rainbow)
        plt.show()

    def get_solution(self):
        domains, constraints, vconstraints = self._get_args()
        if not domains:
            return None
        self._solution = self._solver.get_solution(domains, constraints, vconstraints)
        return self._solution

    def _get_args(self):
        domains = self._variables.copy()
        constraints = self._constraints
        vconstraints = {}
        for variable in domains:
            vconstraints[variable] = []
        for constraint, variables in constraints:
            for variable in variables:
                vconstraints[variable].append((constraint, variables))
        for domain in domains.values():
            domain.reset_state()
        return domains, constraints, vconstraints

