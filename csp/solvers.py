import random
from csp.variables import Unassigned


class Solver(object):
    def __init__(self):
        self.counter = 0

    def get_description(self):
        msg = "%s is an abstract class" % self.__class__.__name__
        raise NotImplementedError(msg)

    def get_solution(self, domains, constraints, vconstraints):
        msg = "%s is an abstract class" % self.__class__.__name__
        raise NotImplementedError(msg)


class MinConflictsSolver(Solver):
    def __init__(self, steps=1000):
        super().__init__()
        self._steps = steps

    def get_description(self):
        return "Minimum Conflicts Algorithm"

    def min_conflict(self, domains, vconstraints):
        self.counter = 0
        assignments = {}
        # Initial assignment
        for variable in domains:
            assignments[variable] = random.choice(domains[variable])
        for _ in range(self._steps):
            conflicted = False
            lst = list(domains.keys())
            random.shuffle(lst)
            for variable in lst:
                # Check if variable is not in conflict
                for constraint, variables in vconstraints[variable]:
                    self.counter = self.counter + 1
                    if not constraint(variables, domains, assignments):
                        break
                else:
                    continue
                # Variable has conflicts. Find values with less conflicts.
                mincount = len(vconstraints[variable])
                minvalues = []
                for value in domains[variable]:
                    assignments[variable] = value
                    count = 0
                    for constraint, variables in vconstraints[variable]:
                        self.counter = self.counter + 1
                        if not constraint(variables, domains, assignments):
                            count += 1
                    if count == mincount:
                        minvalues.append(value)
                    elif count < mincount:
                        mincount = count
                        del minvalues[:]
                        minvalues.append(value)
                # Pick a random one from these values.
                assignments[variable] = random.choice(minvalues)
                conflicted = True
            if not conflicted:
                return assignments
        return None

    def get_solution(self, domains, constraints, vconstraints):
        return self.min_conflict(domains, vconstraints)


class RecursiveBacktrackingSolver(Solver):
    def __init__(self, forwardcheck=True):
        super().__init__()
        self._forward_check = forwardcheck

    def get_description(self):
        return "Recursive Backtracking Algorithm with Forward check: %s" % self._forward_check

    def recursiveBacktracking(self, solutions, domains, vconstraints, assignments, single):
        # Minimum Remaining Values (MRV) heuristics
        lst = [(len(domains[variable]), variable) for variable in domains]
        lst.sort()
        for item in lst:
            if item[-1] not in assignments:
                # Found an unassigned variable. Let's go.
                break
        else:
            # No unassigned variables. We've got a solution.
            solutions.append(assignments.copy())
            return solutions

        variable = item[-1]
        assignments[variable] = Unassigned

        forwardcheck = self._forward_check
        if forwardcheck:
            pushdomains = [domains[x] for x in domains if x not in assignments]
        else:
            pushdomains = None

        for value in domains[variable]:
            assignments[variable] = value
            if pushdomains:
                for domain in pushdomains:
                    domain.push_state()
            for constraint, variables in vconstraints[variable]:
                self.counter = self.counter + 1
                if not constraint(variables, domains, assignments, pushdomains):
                    # Value is not good.
                    break
            else:
                # Value is good. Recurse and get next variable.
                self.recursiveBacktracking(solutions, domains, vconstraints, assignments, single)
                if solutions and single:
                    return solutions
            if pushdomains:
                for domain in pushdomains:
                    domain.pop_state()
        del assignments[variable]
        return solutions

    def get_solution(self, domains, constraints, vconstraints):
        self.counter = 0
        solutions = self.recursiveBacktracking([], domains, vconstraints, {}, False)
        return solutions and solutions[0] or None
